from pydantic import BaseModel, ConfigDict, Field

from .evaluation_schema import Evaluation
from .lecture_schema import Lecture


class CourseBase(BaseModel):
    title: str = Field(
        description="The official title of the course. If the title can't be found, the course code can be used.")
    semester: str | None = Field(
        default=None,
        description="The semester in which the course is offered, like 'Fall 2025', '2025.2' or '2025/2'.")
    archived: bool = Field(
        default=False,
        description="Used by the application for internal control. Preserve default value.")


class CourseCreate(CourseBase):
    owner_uuid: str


class CourseUpdate(BaseModel):
    title: str | None = None
    semester: str | None = None
    archived: bool | None = None


class Course(CourseBase):
    uuid: str
    lectures: list[Lecture] = []
    evaluations: list[Evaluation] = []
    model_config = ConfigDict(from_attributes=True)


class CoursesList(BaseModel):
    courses: list[Course]


class CourseSummary(CourseBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)
