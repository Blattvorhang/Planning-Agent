from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from .question import ExamQuestions


class LearnRequest(BaseModel):
    prompt: str = Field(..., description="用户输入")
    session_id: Optional[str] = Field(None, description="会话ID，用于维持对话状态")


class LearnResponse(BaseModel):
    learning_goal: str
    answer: str
    exam_questions: ExamQuestions
    session_id: Optional[str] = None