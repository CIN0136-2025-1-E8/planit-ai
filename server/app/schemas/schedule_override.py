from datetime import date, time

from pydantic import BaseModel, ConfigDict


class ScheduleOverrideBase(BaseModel):
    override_date: date
    is_cancelled: bool = False
    notes: str | None = None
    new_start_time: time | None = None
    new_end_time: time | None = None
    new_location: str | None = None


class ScheduleOverrideCreate(ScheduleOverrideBase):
    class_id: int


class ScheduleOverrideUpdate(BaseModel):
    is_cancelled: bool | None = None
    notes: str | None = None
    new_start_time: time | None = None
    new_end_time: time | None = None
    new_location: str | None = None


class ScheduleOverride(ScheduleOverrideBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
