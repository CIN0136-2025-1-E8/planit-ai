from datetime import date

from pydantic import BaseModel, ConfigDict


class PersonalEventBase(BaseModel):
    title: str
    description: str | None = None
    event_type: str  # Ex: "Feriado", "Prova", "Entrega", "Recesso"
    start_date: date
    end_date: date | None = None  # Opcional para eventos de um só dia


class PersonalEventCreate(PersonalEventBase):
    # Pode ser associado a um semestre específico ou ser geral
    semester_id: int | None = None


class PersonalEventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    event_type: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class PersonalEvent(PersonalEventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
