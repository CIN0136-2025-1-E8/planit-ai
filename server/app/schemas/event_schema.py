from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime, timedelta


class EventBase(BaseModel):
    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime


class EventCreate(EventBase):
    @field_validator('start_datetime', 'end_datetime')
    def validate_datetimes_are_utc(cls, v: datetime) -> datetime:  # noqa: PyMethodParameters
        if v.tzinfo is None or v.utcoffset() != timedelta(0):
            raise ValueError("Datetime must be in UTC (use 'Z' or '+00:00' offset)")
        return v


class EventCreateInDB(EventBase):
    owner_uuid: str


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
