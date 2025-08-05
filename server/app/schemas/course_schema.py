from pydantic import BaseModel, ConfigDict, Field

from .evaluation_schema import Evaluation, EvaluationGenerate
from .lecture_schema import Lecture, LectureGenerate


class CourseBase(BaseModel):
    title: str = Field(
        description="The official title of the course. If the title can't be found, the course code can be used.")
    semester: str | None = Field(
        default=None,
        description="The semester in which the course is offered, like 'Fall 2025', '2025.2' or '2025/2'.")


class CourseCreate(CourseBase):
    owner_uuid: str


class CourseUpdate(BaseModel):
    title: str | None = None
    semester: str | None = None
    archived: bool | None = None


class CourseGenerate(CourseBase):
    lectures: list[LectureGenerate] = []
    evaluations: list[EvaluationGenerate] = []


class Course(CourseBase):
    uuid: str
    archived: bool = False
    lectures: list[Lecture] = []
    evaluations: list[Evaluation] = []
    model_config = ConfigDict(from_attributes=True)


class CourseSummary(CourseBase):
    uuid: str
    archived: bool = False
    model_config = ConfigDict(from_attributes=True)


class CourseDeleteResponse(CourseSummary):
    deleted_lectures: int | None = None
    deleted_evaluations: int | None = None
    model_config = ConfigDict(from_attributes=True)
