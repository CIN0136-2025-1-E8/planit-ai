from pydantic import BaseModel, ConfigDict

from .evaluation_schema import Evaluation
from .lecture_schema import Lecture


class CourseBase(BaseModel):
    title: str
    semester: str | None = None
    archived: bool = False


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = None
    semester: str | None = None
    archived: bool | None = None


class Course(CourseBase):
    uuid: str
    lectures: list[Lecture] = []
    evaluations: list[Evaluation] = []
    model_config = ConfigDict(from_attributes=True)


class CourseSummary(CourseBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)
