from pydantic import BaseModel, ConfigDict

from app.schemas import Event, Routine, CourseSummary


class UserBase(BaseModel):
    name: str
    nickname: str | None = None
    email: str


class UserCreate(UserBase):
    password: str


class UserCreateInDB(UserBase):
    hashed_password: str
    is_active: bool = True


class UserUpdate(BaseModel):
    name: str | None = None
    nickname: str | None = None
    email: str | None = None
    password: str | None = None


class User(UserBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)


class UserData(UserBase):
    uuid: str
    courses: list[CourseSummary]
    events: list[Event]
    routines: list[Routine]
    model_config = ConfigDict(from_attributes=True)
