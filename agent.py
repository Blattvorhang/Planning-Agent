from typing import TypedDict
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from typing_extensions import Annotated
from abc import ABC, abstractmethod


class State(TypedDict):
    user_input: Annotated[list, add_messages]
    learning_goal: Annotated[list, add_messages]
    feedback: Annotated[list, add_messages]
    learning_plan: Annotated[list, add_messages]
    evaluation_result: Annotated[list, add_messages]
    exam_questions: Annotated[list, add_messages]


class Agent(ABC):
    def __init__(self, llm: AzureChatOpenAI):
        self.llm = llm

    @abstractmethod
    def process(self, state: State) -> State:
        """Process the state and return the updated state"""
        pass


class PlannerAgent(Agent):
    def process(self, state: State) -> State:
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
            state['learning_plan'] = [self.llm.invoke(prompt)]
        else:
            # 初次生成学习目标和学习计划
            goal_prompt = f"用户输入：{user_input}，请生成对应的学习目标。"
            plan_prompt = f"用户输入：{user_input}，请生成对应的学习计划。"
            state['learning_goal'] = [self.llm.invoke(goal_prompt)]
            state['learning_plan'] = [self.llm.invoke(plan_prompt)]
            
        print(f"Planner Agent - learning_goal: {state['learning_goal'][0].content}, learning_plan: {state['learning_plan'][0].content}")
        return state


class EvaluatorAgent(Agent):
    def process(self, state: State) -> State:
        # 评估学习路径或计划的合理性
        learning_goal = state['learning_goal']
        learning_plan = state['learning_plan']
        prompt = f"学习目标是：{learning_goal}，学习计划是：{learning_plan}，请评估该学习计划是否合理，并给出反馈建议。如果合理，请只输出'OK'，否则请输出具体的反馈建议。'"
        state['evaluation_result'] = [self.llm.invoke(prompt)]
        print(f"Evaluator - evaluation_result: {state['evaluation_result'][0].content}")
        return state


class ExaminerAgent(Agent):
    def process(self, state: State) -> State:
        # 根据知识点生成练习或推荐题目
        state['exam_questions'] = ["题目1", "题目2", "题目3"]
        print(f"Examiner - exam_questions: {state['exam_questions']}")
        return state


def user_input_handler(state: State):
    # 确保 user_input 以列表形式添加
    if not state.get('user_input'):
        state['user_input'] = [state['user_input']]
    return state
