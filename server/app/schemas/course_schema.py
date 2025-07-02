from enum import Enum

from pydantic import BaseModel


class EvaluationTypes(Enum):
    EXAM = "exam"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"  # Generic term for the submission of written assignments, problem sets, projects, etc.
    PRESENTATION = "presentation"
    LAB = "lab"


class Evaluation(BaseModel):
    type: EvaluationTypes
    title: str
    start_datetime: str
    end_datetime: str


class Lecture(BaseModel):
    title: str
    start_datetime: str
    end_datetime: str
    summary: str | None = None


class CourseBase(BaseModel):
    title: str
    semester: str | None = None
    lectures: list[Lecture] = []
    evaluations: list[Evaluation] = []


class Course(CourseBase):
    uuid: str


class CoursesList(BaseModel):
    courses: list[Course]
