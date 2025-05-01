import logging

from .base import ReActAgent, State

logger = logging.getLogger(__name__)


class ExaminerAgent(ReActAgent):
    async def process(self, state: State) -> State:
        # 从 state 中获取学习计划
        learning_plan = state['learning_plan']
        # 构建请求模型的提示语
        prompt = f"""
**You are a professional exam question creator. Your task is to design a small set of practice exercises based on the given learning plan or the answer to a user question to help the learner consolidate their knowledge.**  
Make sure that the language used in the output matches the language of the original learning plan.

Given the learning plan/answer: {learning_plan}, your task is to design a small set of practice questions to help reinforce the learner's knowledge.  
The questions should focus on key concepts and important details.

**Instructions:**  
- Generate **3 to 5 questions** in total  
- Focus primarily on **multiple-choice questions** (single-answer) and **fill-in-the-blank questions**  
- For multiple-choice questions:  
  - Provide **3 to 5 answer options**  
  - **Clearly indicate** which option is correct  
- For fill-in-the-blank questions:  
  - Write the question with a blank (use "_____")  
  - Provide the correct answer  
- Questions should be **concise**, **relevant**, and cover **different aspects** of the topic  
- Avoid overly complex or ambiguous questions

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

Please ensure your response is in **valid JSON format** and follows the **exact structure** shown above.
"""
        # 调用模型生成练习题
        result = await self.agent.ainvoke({"messages": prompt})
        # 提取生成的练习题结果
        exam_questions = result['messages'][-1].content
        state['exam_questions'] = exam_questions
        logger.info(f"Examiner - exam_questions: {state['exam_questions']}")
        return state