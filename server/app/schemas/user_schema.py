from typing import Union

from pydantic import BaseModel, ConfigDict

from app.schemas import Event, Routine, CourseSummary, LectureInSchedule, EvaluationInSchedule, EventInSchedule


class UserBase(BaseModel):
    name: str
    nickname: str | None = None
    email: str


class UserCreate(UserBase):
    uuid: str
    hashed_password: str = "A"


class UserUpdate(BaseModel):
    name: str | None = None
    nickname: str | None = None
    email: str | None = None


class User(UserBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)


class UserData(UserBase):
    uuid: str
    courses: list[CourseSummary]
    events: list[Event]
    routines: list[Routine]
    model_config = ConfigDict(from_attributes=True)


ScheduleItems = Union[LectureInSchedule, EvaluationInSchedule, EventInSchedule]


class DailySchedule(BaseModel):
    schedule_items: list[ScheduleItems]


ScheduleResponse = dict[str, list[ScheduleItems]]
