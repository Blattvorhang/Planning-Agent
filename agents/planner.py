from typing import TypedDict
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from typing_extensions import Annotated
from abc import ABC, abstractmethod
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.prebuilt import create_react_agent
from agents.base import ReActAgent, State


class PlannerAgent(ReActAgent):
    async def process(self, state: State) -> State:
        # 调用知识库和 Web 搜索工具
        # 生成学习路径、计划、知识讲解
        user_input = state['user_input']
        feedback = state['feedback']
        evaluation_result = state['evaluation_result'][0].content.strip() if state['evaluation_result'] else ""

        if evaluation_result == "OK":
            # 如果评估通过，直接返回学习计划
            return state

        if feedback:
            # 若有反馈，根据反馈更新学习计划
            prompt = f"用户之前的输入是：{user_input}，反馈是：{feedback}，请更新学习计划。"
            # 确保返回结果为列表形式添加到 learning_plan
            result = await self.agent.ainvoke({"messages": prompt})
            state['learning_plan'] = [result['messages'][1].content]
        else:
            # 初次生成学习目标和学习计划
            goal_prompt = f"用户输入：{user_input}，请分析用户的意图，给出用户对应的学习目标。"
            plan_prompt = f"用户输入：{user_input}，请回答用户输入的问题"
            goal_result = await self.agent.ainvoke({"messages": goal_prompt})
            plan_result = await self.agent.ainvoke({"messages": plan_prompt})
            state['learning_goal'] = [goal_result['messages'][1].content]
            state['learning_plan'] = [plan_result['messages'][1].content]
        print(f"Planner Agent - learning_goal: {state['learning_goal']}, learning_plan: {plan_result}")
        return state