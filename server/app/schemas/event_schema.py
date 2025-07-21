from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    title: str
    description: str | None = None
    start_datetime: str
    end_datetime: str


class EventCreate(EventBase):
    owner_uuid: str


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_datetime: str | None = None
    end_datetime: str | None = None


class Event(EventBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)
