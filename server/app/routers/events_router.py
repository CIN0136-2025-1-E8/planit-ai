from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_db
from app.crud.event import event_crud
from app.schemas.event_schema import EventCreate, EventUpdate, Event
from app.crud.user import user_crud

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
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

@router.get("/", response_model=list[Event])
def read_all_events_by_owner(
    owner_uuid: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    owner = user_crud.get(db, obj_uuid=owner_uuid)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with UUID {owner_uuid} not found."
        )

    events = event_crud.get_events_by_owner(db, owner_uuid=owner_uuid, skip=skip, limit=limit)
    return events

@router.get("/{event_uuid}", response_model=Event)
def read_event_by_uuid(
    event_uuid: str,
    owner_uuid: str,
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

@router.put("/{event_uuid}", response_model=Event)
def update_existing_event(
    event_uuid: str,
    owner_uuid: str,
    event_update: EventUpdate,
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

@router.delete("/{event_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_event(
    event_uuid: str,
    owner_uuid: str,
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
