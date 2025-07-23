from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date, timedelta
from collections import defaultdict

from app.dependencies import get_db
from app.crud.event import event_crud
from app.schemas.event_schema import EventCreate, EventUpdate, Event, EventsByDay
from app.crud.user import user_crud

events_router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

@events_router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_new_event(
    event_in: EventCreate,
    owner_uuid: str,
    db: Session = Depends(get_db)
):
    owner = user_crud.get(db, obj_uuid=owner_uuid)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with UUID {owner_uuid} not found."
        )
    event = event_crud.create(db=db, obj_in=event_in, owner_uuid=owner_uuid)
    return event

@events_router.get("/", response_model=EventsByDay)
def get_events_for_week(
    owner_uuid: str = Query(..., description="UUID do proprietário dos eventos."),
    start_date: date = Query(..., description="Data de início (formato YYYY-MM-DD) para buscar eventos pelos próximos 7 dias."),
    db: Session = Depends(get_db)
):
    """
    Retorna os eventos de um usuário para os 7 dias seguintes (incluindo a data de início),
    agrupados por dia.
    """
    # 1. Verifica se o owner_uuid corresponde a um usuário existente
    owner = user_crud.get(db, obj_uuid=owner_uuid)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with UUID {owner_uuid} not found."
        )

    # 2. Chama o CRUD para obter todos os eventos no período de 7 dias
    all_events = event_crud.get_events_by_owner(
        db,
        owner_uuid=owner_uuid,
        start_date=start_date # Passa apenas a data de início para o CRUD
    )

    # 3. Agrupa os eventos por dia
    events_grouped_by_day = defaultdict(list)
    
    # Preenche o dicionário com os 7 dias, garantindo que todos apareçam no output, mesmo vazios
    for i in range(7):
        current_day = start_date + timedelta(days=i)
        events_grouped_by_day[current_day.isoformat()] = []

    for event in all_events:
        event_day_str = event.start_datetime.date().isoformat()
        
        if start_date <= event.start_datetime.date() <= (start_date + timedelta(days=6)):
            events_grouped_by_day[event_day_str].append(event)
            
    # Ordena o dicionário pelo nome da chave (que são as datas) para uma resposta ordenada
    ordered_events = dict(sorted(events_grouped_by_day.items()))

    return EventsByDay(daily_events=ordered_events)

@events_router.get("/{event_uuid}", response_model=Event)
def read_event_by_uuid(
    event_uuid: str,
    owner_uuid: str = Query(..., description="UUID do proprietário do evento."),
    db: Session = Depends(get_db)
):
    event = event_crud.get_event(db, uuid=event_uuid)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    if event.owner_uuid != owner_uuid:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this event."
        )
    return event

@events_router.put("/{event_uuid}", response_model=Event)
def update_existing_event(
    event_uuid: str,
    event_update: EventUpdate,
    owner_uuid: str = Query(..., description="UUID do proprietário do evento."),
    db: Session = Depends(get_db)
):
    db_event = event_crud.get_event(db, uuid=event_uuid)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    if db_event.owner_uuid != owner_uuid:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this event."
        )

    updated_event = event_crud.update(db=db, db_obj=db_event, obj_in=event_update)
    return updated_event

@events_router.delete("/{event_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_event(
    event_uuid: str,
    owner_uuid: str = Query(..., description="UUID do proprietário do evento."),
    db: Session = Depends(get_db)
):
    db_event = event_crud.get_event(db, uuid=event_uuid)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    if db_event.owner_uuid != owner_uuid:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this event."
        )

    event_crud.remove(db, uuid=event_uuid)
    return {"message": "Event deleted successfully"}
