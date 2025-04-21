import os
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import Literal
import matplotlib.pyplot as plt
import io
from agent import State, PlannerAgent, EvaluatorAgent, ExaminerAgent, user_input_handler


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


if __name__ == "__main__":
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

    # 构建状态图
    graph_builder = StateGraph(State)

    # 创建代理实例
    planner = PlannerAgent(llm)
    evaluator = EvaluatorAgent(llm)
    examiner = ExaminerAgent(llm)

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
