from langgraph.graph import StateGraph, START, END
from .config import get_settings
from agents.base import State, user_input_handler
from agents.planner import PlannerAgent
from agents.evaluator import EvaluatorAgent
from agents.examiner import ExaminerAgent
from langchain_openai import AzureChatOpenAI
import json, asyncio, os
from .models import Literal

def build_llm():
    st = get_settings()
    return AzureChatOpenAI(
        name=st.MODEL_NAME,
        api_key=st.API_KEY,
        azure_endpoint=st.AZURE_ENDPOINT,
        azure_deployment=st.MODEL_NAME,
        api_version="2024-12-01-preview",
        temperature=0.8,
        timeout=90,          # 建议加超时
        max_retries=2,
    )
def route(state: State) -> Literal["evaluator", "examiner"]:
    # 提取评估结果的 content 部分
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
    
async def build_graph():
    llm = build_llm()
    with open("tools/mcp.json") as f:
        tools = json.load(f)['mcpServers']

    planner = PlannerAgent(llm, tools)
    evaluator = EvaluatorAgent(llm)
    examiner = ExaminerAgent(llm, tools)

    # NOTE: 让三个 agent 在应用生命周期内常驻
    await asyncio.gather(planner.start(), evaluator.start(), examiner.start())

    g = StateGraph(State)
    g.add_node("input", user_input_handler)
    g.add_node("planner", planner.process)
    g.add_node("evaluator", evaluator.process)
    g.add_node("examiner", examiner.process)

    g.add_edge(START, "input")
    g.add_edge("input", "planner")
    g.add_conditional_edges("planner", route)   # 你的 route() 直接引用即可
    g.add_edge("evaluator", "planner")
    g.add_edge("examiner", END)

    return g.compile(), (planner, evaluator, examiner)