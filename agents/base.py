from typing import TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from typing_extensions import Annotated
from abc import ABC, abstractmethod
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.prebuilt import create_react_agent


class State(TypedDict):
    user_input: Annotated[list, add_messages]
    learning_goal: Annotated[list, add_messages]
    feedback: Annotated[list, add_messages]
    learning_plan: Annotated[list, add_messages]
    evaluation_result: Annotated[list, add_messages]
    exam_questions: Annotated[list, add_messages]


class ReActAgent(ABC):
    def __init__(self, model:  AzureChatOpenAI, server_config: Optional[dict] = None):
        self.model = model
        self.server_config = server_config
        self.client = None
        self.agent = None

    async def start(self):
        self.client = await MultiServerMCPClient(self.server_config).__aenter__()
        
        self.agent = create_react_agent(
            self.model,
            self.client.get_tools()
        )

    async def close(self):
        if self.client:
            await self.client.__aexit__(None, None, None)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @abstractmethod
    async def process(self, state: dict) -> dict:
        pass
    

def user_input_handler(state: State):
    # 确保 user_input 以列表形式添加
    if not state.get('user_input'):
        state['user_input'] = [state['user_input']]
    return state
