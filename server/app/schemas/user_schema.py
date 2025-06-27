from pydantic import BaseModel, ConfigDict

from schemas import Event, Routine, FileRecord, CourseSummary


class UserBase(BaseModel):
    name: str
    nickname: str | None = None
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    nickname: str | None = None
    email: str | None = None
    password: str | None = None


class User(UserBase):
    uuid: str
    courses: list[CourseSummary]
    events: list[Event]
    routines: list[Routine]
    files: list[FileRecord]
    model_config = ConfigDict(from_attributes=True)


class UserProfile(UserBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)
