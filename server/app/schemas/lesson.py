from datetime import date

from pydantic import BaseModel, ConfigDict


class LessonBase(BaseModel):
    date: date
    topic: str | None = None
    summary: str | None = None
    reading_materials: str | None = None


class LessonCreate(LessonBase):
    class_id: int


class LessonUpdate(BaseModel):
    topic: str | None = None
    summary: str | None = None
    reading_materials: str | None = None


class Lesson(LessonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
