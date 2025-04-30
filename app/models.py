from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class UserPortrait(BaseModel):
    metadata: Dict[str, Any]
    learning_profile: Dict[str, Any]


class LearnRequest(BaseModel):
    prompt: str = Field(..., description="用户输入")
    user_portrait: Optional[UserPortrait] = Field(None, description="用户画像")


class LearnResponse(BaseModel):
    learning_goal: str
    answer: str
    exam_questions: str
    user_portrait: Optional[UserPortrait] = None