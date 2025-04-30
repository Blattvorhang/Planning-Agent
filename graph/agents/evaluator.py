import logging

from .base import ReActAgent, State    


logger = logging.getLogger(__name__)


class EvaluatorAgent(ReActAgent):
    async def process(self, state: State) -> State:
        # 评估学习路径或计划的合理性
        learning_goal = state['learning_goal']
        learning_plan = state['learning_plan']
        prompt = f"""你是一个学习计划评估助手 EvaluatorAgent，专门负责对生成的学习计划或知识讲解内容进行审核和优化建议。
请你评估以下由 PlannerAgent 生成的内容是否合理、完整、清晰。如果以下任意一项存在问题，请给出具体简短的优化建议。

评估维度包括但不限于：
1. 内容是否符合用户需求或目标（目标明确、相关性强）
2. 知识点是否全面、覆盖合理（是否有遗漏）
3. 学习步骤是否合理、有层次（是否过于简略或混乱）
4. 是否需要补充关键点或示例（如缺少重点术语、关键操作）
5. 表述是否简洁清晰，结构是否清楚

输出规则：
- 如果你认为这份学习计划/讲解已经非常合理、无须修改，请只输出一行文本：**OK**
- 否则，请输出**优化建议**，每条建议尽可能简洁，直接指出需要补充或改进的内容。

示例输入：
用户目标：我想掌握 Python 中的字典用法。

PlannerAgent 输出：
\"\"\"
1. 学习 Python 字典的基本结构（键值对形式）
2. 学会访问、添加和修改字典的内容
3. 理解常用方法，如 get(), items(), keys()
\"\"\"

示例输出（不够完善的情况）：
- 建议补充：建议加入“如何安全删除键值对”的知识点。
- 建议补充：可增加典型错误场景及应对（如访问不存在的键）。
- 表达建议：学习步骤建议分阶段列出，更具条理性。

示例输出（内容合理时）：
OK

用户目标：{learning_goal}
PlannerAgent 输出：
{learning_plan}"""
        result  = await self.agent.ainvoke({"messages": prompt})
        state['evaluation_result'] = [result['messages'][-1].content]
        logger.info(f"Evaluator - evaluation_result: {state['evaluation_result']}")
        return state
    