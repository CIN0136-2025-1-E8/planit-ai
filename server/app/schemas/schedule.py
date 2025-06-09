from datetime import time

from pydantic import BaseModel, ConfigDict


class ScheduleBase(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    location: str | None = None


class ScheduleCreate(ScheduleBase):
    class_id: int


class ScheduleUpdate(BaseModel):
    day_of_week: str | None = None
    start_time: time | None = None
    end_time: time | None = None
    location: str | None = None


class Schedule(ScheduleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
