import os
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import Literal
import matplotlib.pyplot as plt
import io
from agents.base import State,user_input_handler
from agents.planner import PlannerAgent
from agents.evaluator import EvaluatorAgent
from agents.examiner import ExaminerAgent
import asyncio

# 修改路由函数
def route(state: State) -> Literal["evaluator", "examiner"]:
    # 提取评估结果的 content 部分
    if len(state["evaluation_result"]) > 2:
        print("\n exceed limit--------goto:examiner")
        return "examiner"
    evaluation_result = state['evaluation_result'][0].content.strip() if state['evaluation_result'] else ""
    if evaluation_result != "OK":
        print("\n --------goto:evaluator")
        return "evaluator"
    else:
        print("\n --------goto:examiner")
        return "examiner"
    

async def main():
    load_dotenv()
    model_name = "gpt-4o-mini"
    llm = AzureChatOpenAI(
        name="gpt-4o-mini",
        api_key=os.getenv("API_KEY"),
        azure_endpoint="https://20242-m9bfmsab-eastus2.cognitiveservices.azure.com/",
        azure_deployment=model_name,
        api_version="2024-12-01-preview",
        temperature=0.8,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    tools = {
            "arxiv-mcp-server": {
            "command": "uv",
            "args": [
                "tool",
                "run",
                "tools/arxiv-mcp-server",
                "--storage-path", "./papers"
            ]
        }

    }

    async with PlannerAgent(llm, tools) as planner, \
               EvaluatorAgent(llm) as evaluator, \
               ExaminerAgent(llm, tools) as examiner:
          # 构建状态图
        graph_builder = StateGraph(State)

        # 添加节点
        graph_builder.add_node("input", user_input_handler)
        graph_builder.add_node("planner", planner.process)
        graph_builder.add_node("evaluator", evaluator.process)
        graph_builder.add_node("examiner", examiner.process)

        # 添加边
        graph_builder.add_edge(START, "input")
        graph_builder.add_edge("input", "planner")
        graph_builder.add_conditional_edges("planner", route)
        graph_builder.add_edge("evaluator", "planner")
        graph_builder.add_edge("examiner", END)

        # 编译图
        graph = graph_builder.compile()

         # 示例输入
        input_state = {
            "user_input": ["我要学习LLM推荐系统的知识"],
            "learning_goal": [],
            "feedback": [],
            "learning_plan": [],
            "evaluation_result": [],
            "exam_questions": [],
        }
        config = {"configurable": {"thread_id": "1"}}
        # 异步运行图
        async for event in graph.astream(input_state, config, stream_mode="values"):
            pass 
    


if __name__ == "__main__":
    asyncio.run(main())
    
  
   

