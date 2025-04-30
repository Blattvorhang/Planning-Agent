import logging

from .base import ReActAgent, State

logger = logging.getLogger(__name__)


class ExaminerAgent(ReActAgent):
    async def process(self, state: State) -> State:
        # 从 state 中获取学习计划
        learning_plan = state['learning_plan']
        # 构建请求模型的提示语
        prompt = f"""你是一个专业的考试出题人，你的任务是根据给定的学习计划或者对用户的问题的回答设计一系列的小练习来帮助学习者巩固知识。你需要注意输出的语言应该和学习计划的语言保持一致。
Given the learning plan/answer: {learning_plan}, your task is to design a small set of practice questions to help reinforce the learner's knowledge. 
The questions should focus on key concepts and important details.

**Instructions:**
- Generate 3-5 questions in total
- Generate mainly **multiple-choice questions** (single-choice) and **fill-in-the-blank questions**
- For multiple-choice questions:
  - Provide 3-5 answer options
  - Clearly indicate which option is correct
- For fill-in-the-blank questions:
  - Provide the question text with a blank space (use "_____")
  - Provide the correct answer
- Questions should be concise, relevant, and cover different aspects of the topic
- Do not generate overly complicated or ambiguous questions

**Required Output Format (JSON):**
{{
    "questions": [
        {{
            "type": "multiple_choice",
            "question_text": "Your question here?",
            "options": [
                {{"label": "A", "content": "Option A content"}},
                {{"label": "B", "content": "Option B content"}},
                {{"label": "C", "content": "Option C content"}}
            ],
            "correct_answer": "B"
        }},
        {{
            "type": "fill_in_blank",
            "question_text": "Question with _____",
            "correct_answer": "answer"
        }}
    ]
}}

Please ensure your response is in valid JSON format and follows the exact structure shown above.
"""
        # 调用模型生成练习题
        result = await self.agent.ainvoke({"messages": prompt})
        # 提取生成的练习题结果
        exam_questions = result['messages'][-1].content
        state['exam_questions'] = exam_questions
        logger.info(f"Examiner - exam_questions: {state['exam_questions']}")
        return state