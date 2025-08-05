from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LectureBase(BaseModel):
    title: str
    start_datetime: datetime
    end_datetime: datetime
    summary: str | None = None


class LectureCreate(LectureBase):
    course_uuid: str


class LectureGenerate(BaseModel):
    title: str = Field(
        description="The main topic or title of the lecture.")
    start_datetime: str = Field(
        description="The start date and time of the lecture in ISO 8601 format.")
    end_datetime: str = Field(
        description="The end date and time of the lecture in ISO 8601 format.")
    summary: str | None = Field(
        default=None,
        description="A brief summary of the lecture's content.")


class LectureUpdate(BaseModel):
    title: str | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    summary: str | None = None
    present: bool | None = None


class Lecture(LectureBase):
    uuid: str
    present: bool | None = None
    model_config = ConfigDict(from_attributes=True)
