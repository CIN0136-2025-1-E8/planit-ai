from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EvaluationTypes(Enum):
    EXAM = "exam"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"  # Generic term for the submission of written assignments, problem sets, projects, etc.
    PRESENTATION = "presentation"
    LAB = "lab"


class EvaluationBase(BaseModel):
    type: EvaluationTypes = Field(
        description="The type of evaluation. 'assignment' is a generic term for the submission of written assignments, problem sets, projects and more.")
    title: str = Field(
        description="The specific title of the evaluation (e.g., 'Midterm Exam', 'Project 1').")
    start_datetime: str = Field(
        description="The start date and time for the evaluation in ISO 8601 format.")
    end_datetime: str = Field(
        description="The end date and time for the evaluation in ISO 8601 format, which is typically the deadline.")


class EvaluationCreate(EvaluationBase):
    course_uuid: str


class EvaluationUpdate(BaseModel):
    type: str | None
    title: str | None
    start_datetime: str | None
    end_datetime: str | None
    present: bool | None = None


class Evaluation(EvaluationBase):
    uuid: str
    present: bool | None = None
    model_config = ConfigDict(from_attributes=True)
