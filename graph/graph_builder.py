from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, START, END

import matplotlib.pyplot as plt
import io
import json, asyncio

from graph.agents.base import State, user_input_handler
from graph.agents.planner import PlannerAgent
from graph.agents.evaluator import EvaluatorAgent
from graph.agents.examiner import ExaminerAgent
from graph.agents.investigator import InvestigatorAgent

from typing_extensions import Literal
from graph.config import get_settings


def build_llm():
    settings = get_settings()
    return AzureChatOpenAI(
        name=settings.MODEL_NAME,
        api_key=settings.API_KEY,
        azure_endpoint=settings.AZURE_ENDPOINT,
        azure_deployment=settings.MODEL_NAME,
        api_version="2024-12-01-preview",
        temperature=0.8,
        timeout=90,          # 建议加超时
        max_retries=2,
    )


def route_after_input(state: State) -> Literal["investigator", "planner"]:
    """根据是否有用户画像决定路由"""
    if not state.get("user_portrait"):
        return "investigator"
    return "planner"


def route_after_investigator(state: State) -> Literal["investigator", "planner"]:
    """根据用户画像是否完成决定路由"""
    if not state.get("user_portrait") or not state["user_portrait"].get("learning_profile"):
        return "investigator"
    return "planner"


def route_after_planner(state: State) -> Literal["evaluator", "examiner"]:
    if len(state["evaluation_result"]) > 2:
        #print("\n exceed limit--------goto:examiner")
        return "examiner"
    evaluation_result = state['evaluation_result'][0].content.strip() if state['evaluation_result'] else ""
    if evaluation_result != "OK":
        #print("\n --------goto:evaluator")
        return "evaluator"
    else:
        #print("\n --------goto:examiner")
        return "examiner"
    

def plot_graph(graph: StateGraph):
    plt.figure(figsize=(10, 6))
    img_data = graph.draw_mermaid_png()
    img = plt.imread(io.BytesIO(img_data))
    plt.imshow(img)
    plt.show()

    
async def build_graph(plot: bool = False):
    llm = build_llm()
    with open("tools/mcp.json") as f:
        tools = json.load(f)['mcpServers']

    investigator = InvestigatorAgent(llm)
    planner = PlannerAgent(llm, tools)
    evaluator = EvaluatorAgent(llm)
    examiner = ExaminerAgent(llm, tools)

    # NOTE: 让所有 agent 在应用生命周期内常驻
    await asyncio.gather(
        investigator.start(),
        planner.start(),
        evaluator.start(),
        examiner.start()
    )

    graph_builder = StateGraph(State)
    graph_builder.add_node("input", user_input_handler)
    graph_builder.add_node("investigator", investigator.process)
    graph_builder.add_node("planner", planner.process)
    graph_builder.add_node("evaluator", evaluator.process)
    graph_builder.add_node("examiner", examiner.process)

    graph_builder.add_edge(START, "input")
    graph_builder.add_conditional_edges(
        "input",
        route_after_input,
        {
            "investigator": "investigator",
            "planner": "planner"
        }
    )
    graph_builder.add_conditional_edges(
        "investigator",
        route_after_investigator,
        {
            "investigator": "investigator",
            "planner": "planner"
        }
    )
    graph_builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "evaluator": "evaluator",
            "examiner": "examiner"
        }
    )
    graph_builder.add_edge("evaluator", "planner")
    graph_builder.add_edge("examiner", END)

    graph = graph_builder.compile()
    if plot:
        plot_graph(graph.get_graph())
    
    return graph, (investigator, planner, evaluator, examiner)


if __name__ == "__main__":
    asyncio.run(build_graph(plot=True))
