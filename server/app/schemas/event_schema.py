from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from uuid import UUID


class EventBase(BaseModel):
    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None


class Event(EventBase):
    uuid: str
    owner_uuid: str
    model_config = ConfigDict(from_attributes=True)


class EventsByDay(BaseModel):
    # A chave do dicionário será a data (como string 'YYYY-MM-DD')
    # O valor será uma lista de objetos Event (usando o schema Event acima)
    daily_events: dict[str, list[Event]] = {}
