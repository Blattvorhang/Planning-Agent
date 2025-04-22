from typing import TypedDict
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from typing_extensions import Annotated
from abc import ABC, abstractmethod
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.prebuilt import create_react_agent
from agents.base import ReActAgent, State    
   
class EvaluatorAgent(ReActAgent):
    async def process(self, state: State) -> State:
        # 评估学习路径或计划的合理性
        learning_goal = state['learning_goal']
        learning_plan = state['learning_plan']
        prompt = f"学习目标是：{learning_goal}，学习计划是：{learning_plan}，请评估该学习计划是否合理，并给出反馈建议。如果合理，请只输出'OK'，否则请输出具体的反馈建议。'"
        result  = await self.agent.ainvoke({"messages": prompt})
        state['evaluation_result'] = [result['messages'][1].content]
        print(f"Evaluator - evaluation_result: {state['evaluation_result']}")
        return state
    