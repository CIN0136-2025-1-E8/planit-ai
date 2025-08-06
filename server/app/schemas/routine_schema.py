from enum import Enum

from pydantic import BaseModel, ConfigDict


class RoutineWeekdays(Enum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 4
    WEDNESDAY = 8
    THURSDAY = 16
    FRIDAY = 32
    SATURDAY = 64


class RoutineBase(BaseModel):
    title: str
    description: str | None = None
    flexible: bool
    start_time: str
    end_time: str
    days_of_the_week: int


class RoutineCreate(RoutineBase):
    pass


class RoutineCreateInDB(RoutineBase):
    owner_uuid: str


class RoutineUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    flexible: bool | None = None
    start_time: str | None = None
    end_time: str | None = None
    days_of_the_week: int | None = None


class Routine(RoutineBase):
    uuid: str
    owner_uuid: str
    model_config = ConfigDict(from_attributes=True)
