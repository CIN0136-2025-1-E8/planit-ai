from typing import List

from pydantic import BaseModel, ConfigDict

from .lesson import Lesson
from .schedule import Schedule
from .schedule_override import ScheduleOverride


class ClassBase(BaseModel):
    class_title: str
    class_code: str | None = None
    professor_name: str | None = None


class ClassCreate(ClassBase):
    semester_id: int


class ClassUpdate(BaseModel):
    class_title: str | None = None
    class_code: str | None = None
    professor_name: str | None = None


class Class(ClassBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ClassWithDetails(Class):
    schedules: List[Schedule] = []
    lessons: List[Lesson] = []
    overrides: List[ScheduleOverride] = []
