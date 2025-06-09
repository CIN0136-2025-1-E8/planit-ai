from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict

from .class_ import ClassWithDetails
from .personal_event import PersonalEvent


class SemesterBase(BaseModel):
    name: str
    start_date: date
    end_date: date


class SemesterCreate(SemesterBase):
    pass


class SemesterUpdate(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class Semester(SemesterBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SemesterWithDetails(Semester):
    classes: List[ClassWithDetails] = []
    personal_events: List[PersonalEvent] = []
