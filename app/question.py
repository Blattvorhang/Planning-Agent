from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_IN_BLANK = "fill_in_blank"


class Option(BaseModel):
    label: str  # A, B, C, D...
    content: str


class Question(BaseModel):
    type: QuestionType
    question_text: str
    options: Optional[List[Option]] = None  # For multiple choice questions
    correct_answer: str  # For multiple choice: label (e.g. "B"); For fill in blank: the answer


class ExamQuestions(BaseModel):
    questions: List[Question]