from datetime import date, time
from typing import List

from pydantic import BaseModel, Field


class ScheduleImport(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    location: str | None = None


class LessonImport(BaseModel):
    date: date
    topic: str | None = None
    summary: str | None = None
    reading_materials: List[str] = []


class PersonalEventImport(BaseModel):
    title: str
    description: str | None = None
    event_type: str
    start_date: date
    end_date: date | None = None


class ClassImport(BaseModel):
    class_title: str
    class_code: str | None = None
    professor_name: str | None = None
    schedules: List[ScheduleImport] = []
    lessons: List[LessonImport] = []


class SemesterImport(BaseModel):
    name: str
    start_date: date
    end_date: date
    classes: List[ClassImport] = []
    personal_events: List[PersonalEventImport] = []


class FullPlanImport(BaseModel):
    semesters: List[SemesterImport] = Field(default=[], title="Lista de Semestres")
    general_personal_events: List[PersonalEventImport] = Field(default=[], title="Eventos Gerais (sem semestre)")
