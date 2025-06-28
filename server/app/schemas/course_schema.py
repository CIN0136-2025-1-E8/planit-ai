import uuid

from pydantic import BaseModel, ConfigDict

from schemas import Evaluation, Lecture


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
    course_uuid: uuid.UUID
    lectures: list[Lecture] = []
    evaluations: list[Evaluation] = []
    model_config = ConfigDict(from_attributes=True)


class CourseSummary(CourseBase):
    course_uuid: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
