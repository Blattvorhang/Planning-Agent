import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import Annotated,Literal  
import matplotlib.pyplot as plt
import io


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

class State(TypedDict):
    user_input: Annotated[list, add_messages]
    learning_goal: Annotated[list, add_messages]
    feedback: Annotated[list, add_messages]
    learning_plan: Annotated[list, add_messages]
    evaluation_result: Annotated[list, add_messages]
    exam_questions: Annotated[list, add_messages]

# User 模块函数
def user_input_handler(state: State):
    # 确保 user_input 以列表形式添加
    if not state.get('user_input'):
        state['user_input'] = [state['user_input']]
    return state

# Planner Agent 模块函数
def planner_agent(state: State):
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
        state['learning_plan'] = [llm.invoke(prompt)]
    else:
        # 初次生成学习目标和学习计划
        goal_prompt = f"用户输入：{user_input}，请生成对应的学习目标。"
        plan_prompt = f"用户输入：{user_input}，请生成对应的学习计划。"
        state['learning_goal'] = [llm.invoke(goal_prompt)]
        state['learning_plan'] = [llm.invoke(plan_prompt)]
    print(f"Planner Agent - learning_goal: {state['learning_goal'][0].content}, learning_plan: {state['learning_plan'][0].content}")
    return state

# Evaluator 模块函数
def evaluator(state: State) -> Optional[State | Command]: 
    # 评估学习路径或计划的合理性
    learning_goal = state['learning_goal']
    learning_plan = state['learning_plan']
    prompt = f"学习目标是：{learning_goal}，学习计划是：{learning_plan}，请评估该学习计划是否合理，并给出反馈建议。如果合理，请只输出'OK'，否则请输出具体的反馈建议。'"
    state['evaluation_result'] =  [llm.invoke(prompt)]
    print(f"Evaluator - evaluation_result: {state['evaluation_result'][0].content}")
    return state
    

# Examiner 模块函数
def examiner(state: State):
    # 根据知识点生成练习或推荐题目
    state['exam_questions'] = ["题目1", "题目2", "题目3"]
    print(f"Examiner - exam_questions: {state['exam_questions']}")
    return state

# 构建状态图
graph_builder = StateGraph(State)

# 添加节点
graph_builder.add_node("input", user_input_handler)
graph_builder.add_node("planner", planner_agent)
graph_builder.add_node("evaluator", evaluator)
graph_builder.add_node("examiner", examiner)

# 修改路由函数
def route(state: State) -> Literal["evaluator", "examiner"]:
    # 提取评估结果的 content 部分
    evaluation_result = state['evaluation_result'][0].content.strip() if state['evaluation_result'] else ""
    if evaluation_result != "OK":
        print("\n --------goto:evaluator")
        return "evaluator"
    else:
        print("\n --------goto:examiner")
        return "examiner"
    

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
    "user_input": ["我想学习 Python 编程"],
    "learning_goal": [],
    "feedback": [],
    "learning_plan": [],
    "evaluation_result": [],
    "exam_questions": [],
}
config = {"configurable": {"thread_id": "1"}}

# 运行图
# result = graph.invoke(input_state)

# print(result)

events = graph.stream(
    input_state,
    config,
    stream_mode="values",
)


# 获取图片的二进制数据
img_data = graph.get_graph().draw_mermaid_png()
# 将二进制数据转换为图像对象
img = plt.imread(io.BytesIO(img_data))

# 使用 matplotlib 显示图像
plt.imshow(img)
plt.axis('off')  # 隐藏坐标轴
plt.show()

for event in events:
    pass