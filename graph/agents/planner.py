import logging
from .base import ReActAgent, State

logger = logging.getLogger(__name__)


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
            goal_prompt_zh = f"""你是一个智能学习助手，负责根据用户的输入分析和提炼他们的学习目标，并细化目标中的关键内容。
任务要求如下：
- 从用户输入中提取并明确学习目标。
- 判断哪些目标是显性目标（直接提到的）和隐性目标（通过推理或问题提炼出来的）。
- 通过目标分析，帮助用户确定学习路径或进一步探讨内容。

输出需要满足以下要求：
- 提取出一个或多个学习目标。
- 每个目标要明确、具体。
- 如果是隐性目标，请基于上下文推测并补充相关目标。
- 输出格式需要包括目标描述和目标类型（显性或隐性）。

示例输入：
“我想掌握 Python 编程，尤其是面向对象的编程和数据分析。我也想了解如何用 Python 做机器学习。”

示例输出：
1. 学习目标：掌握 Python 编程基础，包含语法、数据结构、控制流。
   - 类型：显性目标
2. 学习目标：理解 Python 面向对象编程（OOP）概念，如类、继承、封装等。
   - 类型：显性目标
3. 学习目标：学习如何使用 Python 进行数据分析，掌握 Pandas 和 Numpy 库。
   - 类型：隐性目标（推测用户想了解数据分析工具）
4. 学习目标：了解如何使用 Python 进行机器学习，掌握机器学习算法和框架（如 Scikit-learn）。
   - 类型：隐性目标（推测用户希望学习机器学习）

用户输入：{user_input}"""
            
            goal_prompt = f"""
**You are an intelligent learning assistant. Your task is to analyze the user's input, extract and clarify their learning goals, and break down key components within those goals.**

**Task Requirements:**  
- Extract and clearly define the learning goals from the user's input.  
- Distinguish between explicit goals (directly mentioned) and implicit goals (inferred or derived from the context).  
- Use goal analysis to help guide the user's learning path or suggest areas for further exploration.

**Output Requirements:**  
- Identify one or more specific and well-defined learning goals.  
- Label each goal with its type: **explicit** or **implicit**.  
- If implicit goals are inferred, provide reasonable justification based on the context.  
- Use the following structured format:

**Example Input:**  
“I want to master Python programming, especially object-oriented programming and data analysis. I also want to understand how to do machine learning with Python.”

**Example Output:**  
1. Learning Goal: Master the basics of Python programming, including syntax, data structures, and control flow.  
   - Type: Explicit  
2. Learning Goal: Understand Python object-oriented programming (OOP) concepts such as classes, inheritance, and encapsulation.  
   - Type: Explicit  
3. Learning Goal: Learn how to perform data analysis using Python, including tools like Pandas and Numpy.  
   - Type: Implicit (inferred interest in specific tools for data analysis)  
4. Learning Goal: Understand how to apply Python to machine learning, including learning algorithms and frameworks like Scikit-learn.  
   - Type: Implicit (inferred desire to learn ML techniques and tools)

**User Input:**  
{user_input}
"""

            plan_prompt_zh =  f"""你是一个教育助手，负责根据用户的输入生成学习计划，或者在用户提出问题时进行知识讲解。

任务要求如下：
- 根据用户的学习目标生成详细的学习计划，涵盖所需的知识点和学习路径。
- 在用户提出问题时，提供相关的知识讲解，帮助用户理解某个概念或技术。
- 对于学习计划，确保包括目标、时间分配、参考资料等。

输出需要满足以下要求：
- 如果是学习计划生成，输出格式为：
  1. 学习目标：
     - 描述目标
     - 学习步骤（分解任务）
     - 推荐学习资源（如课程、书籍、工具）
     - 时间建议
- 如果是问题回答，直接给出详细易懂的回答。

示例输入：
“我想学会用 Python 做数据分析，需要掌握 Pandas 和 Numpy。”

示例输出：
学习计划：
1. 学习目标：掌握 Pandas 数据分析库
   - 学习步骤：
     - 学习 Pandas 的数据结构（Series, DataFrame）
     - 学习数据清洗、缺失值处理、数据选择等基础操作
     - 学习如何进行数据可视化（Pandas 与 Matplotlib 集成）
   - 推荐学习资源：
     - 《Python for Data Analysis》书籍
     - 在线教程（如 Coursera 的 Pandas 课程）
   - 时间建议：2 周

2. 学习目标：掌握 Numpy 数值计算库
   - 学习步骤：
     - 学习 Numpy 数组的基础操作和索引
     - 学习线性代数、矩阵运算、广播机制等高级用法
   - 推荐学习资源：
     - 《NumPy官方文档》
     - 在线教程（如 Kaggle 的 Numpy 基础）
   - 时间建议：1 周

回答问题：
**问题：如何使用 Python 处理缺失值？**
- 在 Python 中，处理缺失值常用的库是 Pandas。你可以使用 `fillna()` 方法填充缺失值，或者使用 `dropna()` 删除缺失值行或列。
- 示例代码：
```python
import pandas as pd
data = pd.DataFrame({{'A': [1, 2, None], 'B': [4, None, 6]}})
data.fillna(0, inplace=True)  # 填充缺失值为 0
用户输入：{user_input}"""
            
            plan_prompt = f"""
**You are an educational assistant responsible for generating learning plans based on user input or providing knowledge explanations when users ask questions.**

**Task Requirements:**  
- Generate a detailed learning plan based on the user's learning goal, covering the required knowledge points and learning path.  
- When the user asks a question, provide a clear and relevant explanation to help them understand a concept or technique.  
- For learning plans, ensure the output includes goals, step-by-step learning tasks, recommended resources, and time allocation.

**Output Requirements:**  
- If the task is to generate a learning plan, use the following format:  
  1. **Learning Goal:**  
     - Goal description  
     - Learning steps (task breakdown)  
     - Recommended resources (e.g., courses, books, tools)  
     - Suggested time allocation  
- If the task is answering a question, provide a clear, detailed, and easy-to-understand explanation directly.

**Example Input:**  
"I want to learn how to do data analysis using Python, and I need to master Pandas and Numpy."

**Example Output:**  
**Learning Plan:**  
1. **Learning Goal:** Master the Pandas data analysis library  
   - **Learning Steps:**  
     - Learn Pandas data structures (Series, DataFrame)  
     - Practice basic operations: data cleaning, handling missing values, data selection  
     - Learn data visualization with Pandas (integration with Matplotlib)  
   - **Recommended Resources:**  
     - *Python for Data Analysis* (book)  
     - Online tutorials (e.g., Pandas course on Coursera)  
   - **Time Suggestion:** 2 weeks

2. **Learning Goal:** Master the Numpy numerical computation library  
   - **Learning Steps:**  
     - Learn basic array operations and indexing in Numpy  
     - Explore advanced features: linear algebra, matrix operations, broadcasting  
   - **Recommended Resources:**  
     - *Official NumPy Documentation*  
     - Online tutorials (e.g., Numpy basics on Kaggle)  
   - **Time Suggestion:** 1 week

**Question Answering:**  
**Question:** How do you handle missing values in Python?  
- In Python, the Pandas library is commonly used to handle missing values. You can use the `fillna()` method to fill in missing values or `dropna()` to remove rows or columns with missing data.  
- Example code:  
```python
import pandas as pd  
data = pd.DataFrame({{'A': [1, 2, None], 'B': [4, None, 6]}})
data.fillna(0, inplace=True)  # Fill missing values with 0  
```

**User Input:** {user_input}
"""
            
            goal_result = await self.agent.ainvoke({"messages": goal_prompt})
            plan_result = await self.agent.ainvoke({"messages": plan_prompt})
            logger.info(f"Planner - goal:{goal_result}")
            logger.info(f"Planner - plan:{plan_result}")
            state['learning_goal'] = [goal_result['messages'][-1].content]
            state['learning_plan'] = [plan_result['messages'][-1].content]
            
        return state