from enum import Enum

from pydantic import BaseModel, Field


class EvaluationTypes(Enum):
    EXAM = "exam"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"  # Generic term for the submission of written assignments, problem sets, projects, etc.
    PRESENTATION = "presentation"
    LAB = "lab"


class Evaluation(BaseModel):
    type: EvaluationTypes = Field(
        description="The type of evaluation. 'assignment' is a generic term for the submission of written assignments, problem sets, projects and more.")
    title: str = Field(
        description="The specific title of the evaluation (e.g., 'Midterm Exam', 'Project 1').")
    start_datetime: str = Field(
        description="The start date and time for the evaluation in ISO 8601 format.")
    end_datetime: str = Field(
        description="The end date and time for the evaluation in ISO 8601 format, which is typically the deadline.")


class Lecture(BaseModel):
    title: str = Field(
        description="The main topic or title of the lecture.")
    start_datetime: str = Field(
        description="The start date and time of the lecture in ISO 8601 format.")
    end_datetime: str = Field(
        description="The end date and time of the lecture in ISO 8601 format.")
    summary: str | None = Field(
        default=None,
        description="A brief summary of the lecture's content.")


class CourseBase(BaseModel):
    title: str = Field(
        description="The official title of the course. If the title can't be found, the course code can be used.")
    semester: str | None = Field(
        default=None,
        description="The semester in which the course is offered, like 'Fall 2025', '2025.2' or '2025/2'.")
    lectures: list[Lecture] = Field(
        default=[],
        description="A list of all lectures scheduled for the course.")
    evaluations: list[Evaluation] = Field(
        default=[],
        description="A list of all evaluations, such as exams, quizzes, and assignments for the course.")


class Course(CourseBase):
    uuid: str


class CoursesList(BaseModel):
    courses: list[Course]
