from pydantic import BaseModel, Field
from typing import List, Any
from typing_extensions import Literal


class LearnRequest(BaseModel):
    prompt: str = Field(..., description="用户输入")


class LearnResponse(BaseModel):
    learning_goal: str
    answer: str
    exam_questions: str