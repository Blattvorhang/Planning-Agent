from typing import TypedDict
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from typing_extensions import Annotated
from abc import ABC, abstractmethod
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.prebuilt import create_react_agent
from agents.base import ReActAgent, State


class ExaminerAgent(ReActAgent):
    async def process(self, state: State) -> State:
        # 根据知识点生成练习或推荐题目
        state['exam_questions'] = ["题目1", "题目2", "题目3"]
        print(f"Examiner - exam_questions: {state['exam_questions']}")
        return state