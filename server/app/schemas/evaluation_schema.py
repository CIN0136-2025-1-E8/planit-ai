import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict


class EvaluationTypes(Enum):
    EXAM = "exam"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"  # Generic term for the submission of written assignments, problem sets, projects, etc.
    PRESENTATION = "presentation"
    LAB = "lab"


class EvaluationBase(BaseModel):
    type: str
    title: str
    start_datetime: str
    end_datetime: str
    present: bool | None = None


class EvaluationCreate(EvaluationBase):
    course_uuid: uuid.UUID


class EvaluationUpdate(BaseModel):
    type: str | None
    title: str | None
    start_datetime: str | None
    end_datetime: str | None
    present: bool | None = None


class Evaluation(EvaluationBase):
    evaluation_uuid: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
