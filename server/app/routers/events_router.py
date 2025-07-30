from datetime import date, timedelta, datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException, status, Query, Form
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import get_event_crud, CRUDEvent
from app.dependencies import get_db
from app.models import User
from app.schemas import EventCreate, EventCreateInDB, EventUpdate, Event, EventsByDay

events_router = APIRouter(
    prefix="/event",
    tags=["Event"],
)


@events_router.get("/", response_model=Event)
def get_event(
        event_uuid: str = Form(),
        event_crud: CRUDEvent = Depends(get_event_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
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


@events_router.put("/", response_model=Event)
def update_event(
        event_uuid: str = Form(),
        new_title: str | None = Form(None),
        new_description: str | None = Form(None),
        new_start_datetime: datetime | None = Form(None),
        new_end_datetime: datetime | None = Form(None),
        event_crud: CRUDEvent = Depends(get_event_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    event_new_data: EventUpdate = EventUpdate(
        title=new_title,
        description=new_description,
        start_datetime=new_start_datetime,
        end_datetime=new_end_datetime,
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_event = event_crud.get(db, obj_uuid=event_uuid)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    updated_event = event_crud.update(db=db, db_obj=db_event, obj_in=event_new_data)
    return updated_event


@events_router.post("/", response_model=Event)
def create_event(
        title: str = Form(),
        description: str | None = Form(None),
        start_datetime: datetime = Form(),
        end_datetime: datetime = Form(),
        event_crud: CRUDEvent = Depends(get_event_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    event_in: EventCreate = EventCreate(
        title=title,
        description=description,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    event_create: EventCreateInDB = EventCreateInDB(**event_in.model_dump(), owner_uuid=user.uuid)
    event = event_crud.create(db=db, obj_in=event_create)
    return event


@events_router.delete("/", response_model=Event)
def delete_event(
        event_uuid: str = Form(),
        event_crud: CRUDEvent = Depends(get_event_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    event = event_crud.remove(db, obj_uuid=event_uuid)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event


@events_router.get("/week", response_model=EventsByDay)
def get_events_for_week(
        start_date: date = Query(
            ...,
            description="The start date for the 7-day period (format YYYY-MM-DD)."
        ),
        timezone: str = Query(
            ...,
            description="The client's IANA timezone name (e.g., 'America/Sao_Paulo', 'Europe/Paris')."
        ),
        event_crud: CRUDEvent = Depends(get_event_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """
    Returns a user's events for the next 7 days, interpreted according to the client's timezone.
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        client_tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid timezone identifier: '{timezone}'"
        )

    start_of_period_local = datetime.combine(start_date, time.min, tzinfo=client_tz)

    end_date = start_date + timedelta(days=7)
    end_of_period_local = datetime.combine(end_date, time.min, tzinfo=client_tz)

    start_utc = start_of_period_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_of_period_local.astimezone(ZoneInfo("UTC"))

    all_events = event_crud.get_events_by_owner(
        db,
        owner_uuid=user.uuid,
        start_utc=start_utc,
        end_utc=end_utc,
        limit=1000
    )

    events_grouped_by_day = {
        (start_date + timedelta(days=i)).isoformat(): [] for i in range(7)
    }

    for event in all_events:
        local_datetime = event.start_datetime.astimezone(client_tz)
        event_day_str = local_datetime.date().isoformat()

        if event_day_str in events_grouped_by_day:
            events_grouped_by_day[event_day_str].append(event)

    return EventsByDay(daily_events=events_grouped_by_day)
