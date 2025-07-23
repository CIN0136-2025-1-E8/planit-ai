from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date, timedelta, datetime
from collections import defaultdict

from app.dependencies import get_db
from app.core.security import get_current_user
from app.crud.event import event_crud
from app.models import User
from app.schemas.event_schema import EventCreate, EventCreateInDB, EventUpdate, Event, EventsByDay

events_router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

@events_router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_new_event(
    event_in: EventCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    event_create: EventCreateInDB = EventCreateInDB(**event_in.model_dump(), owner_uuid=user.uuid)
    event = event_crud.create(db=db, obj_in=event_create)
    return event

@events_router.get("/", response_model=EventsByDay)
def get_events_for_week(
    start_date: date = Query(..., description="Data de início (formato YYYY-MM-DD) para buscar eventos pelos próximos 7 dias."),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os eventos de um usuário para os 7 dias seguintes (incluindo a data de início),
    agrupados por dia.
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # 2. Chama o CRUD para obter todos os eventos no período de 7 dias
    all_events = event_crud.get_events_by_owner(
        db,
        owner_uuid=user.uuid,
        start_date=start_date # Passa apenas a data de início para o CRUD
    )

    # 3. Agrupa os eventos por dia
    events_grouped_by_day = defaultdict(list)
    
    # Preenche o dicionário com os 7 dias, garantindo que todos apareçam no output, mesmo vazios
    for i in range(7):
        current_day = start_date + timedelta(days=i)
        events_grouped_by_day[current_day.isoformat()] = []

    for event in all_events:
        try:
            # Assumimos que a string está em formato ISO 8601
            event_datetime_obj = datetime.fromisoformat(event.start_datetime)
            event_day_str = event_datetime_obj.date().isoformat()
        except ValueError:
            # Se a string não estiver em formato ISO 8601, lide com o erro
            print(f"ATENÇÃO: Formato de data inválido no DB para evento {event.uuid}: {event.start_datetime}")
            continue
        
        if start_date <= event_datetime_obj.date() <= (start_date + timedelta(days=6)):
            events_grouped_by_day[event_day_str].append(event)
            
    # Ordena o dicionário pelo nome da chave (que são as datas) para uma resposta ordenada
    ordered_events = dict(sorted(events_grouped_by_day.items()))

    return EventsByDay(daily_events=ordered_events)

@events_router.get("/{event_uuid}", response_model=Event)
def read_event_by_uuid(
    event_uuid: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    event = event_crud.get(db, obj_uuid=event_uuid)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@events_router.put("/{event_uuid}", response_model=Event)
def update_existing_event(
    event_uuid: str,
    event_update: EventUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_event = event_crud.get(db, obj_uuid=event_uuid)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    updated_event = event_crud.update(db=db, db_obj=db_event, obj_in=event_update)
    return updated_event

@events_router.delete("/{event_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_event(
    event_uuid: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    event = event_crud.remove(db, obj_uuid=event_uuid)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return {"message": "Event deleted successfully"}
