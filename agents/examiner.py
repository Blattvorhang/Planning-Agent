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
        # 从 state 中获取学习计划
        learning_plan = state['learning_plan']
        # 构建请求模型的提示语
        prompt = f"""你是一个专业的考试出题人，你的任务是根据给定的学习计划或者对用户的问题的回答设计一系列的小练习来帮助学习者巩固知识。你需要注意输出的语言应该和学习计划的语言保持一致。
Given the learning plan/answer: {learning_plan}, your task is to design a small set of practice questions to help reinforce the learner's knowledge. 
The questions should focus on key concepts and important details.

**Instructions:**
- Generate mainly **multiple-choice questions** (single-choice or multiple-choice) and **fill-in-the-blank questions**.
- For multiple-choice questions:
  - Provide 1 question and 3-5 answer options.
  - Clearly indicate which option is correct.
- For fill-in-the-blank questions:
  - Provide the question text with a blank space.
  - Provide the correct answer separately.
- Questions should be concise, relevant, and cover different aspects of the topic.
- Do not generate overly complicated or ambiguous questions.
- Only output the questions and answers, do not add extra explanations unless explicitly requested.

**Expected Output Format:**
1. [Multiple Choice] Question text
   - A. Option A
   - B. Option B
   - C. Option C
   - D. Option D
   - Correct Answer: B

2. [Fill in the Blank] Question text with _____
   - Correct Answer: [answer]
"""
        # 调用模型生成练习题
        result = await self.agent.ainvoke({"messages": prompt})
        # 提取生成的练习题结果
        exam_questions = result['messages'][1].content
        state['exam_questions'] = exam_questions
        print(f"Examiner - exam_questions: {state['exam_questions']}")
        return state