import uuid

from pydantic import BaseModel, ConfigDict


class LectureBase(BaseModel):
    title: str
    start_datetime: str
    end_datetime: str
    summary: str | None = None
    present: bool | None = None


class LectureCreate(LectureBase):
    course_uuid: uuid.UUID


class LectureUpdate(BaseModel):
    title: str | None = None
    start_datetime: str | None = None
    end_datetime: str | None = None
    summary: str | None = None
    present: bool | None = None


class Lecture(LectureBase):
    lecture_uuid: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
