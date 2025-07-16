from typing import Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.event_model import Event
from app.schemas.event_schema import EventCreate, EventUpdate

class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def create(self, db: Session, *, obj_in: EventCreate, owner_uuid: str) -> Event:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(
            **obj_in_data,
            owner_uuid=owner_uuid 
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_event(self, db: Session, uuid: str) -> Event | None:
        query = select(self.model).filter(self.model.uuid == uuid)
        result = db.execute(query).scalars().first()
        return result

    def get_events_by_owner(self, db: Session, owner_uuid: str, skip: int = 0, limit: int = 100) -> list[Event]:
        query = select(self.model).filter(self.model.owner_uuid == owner_uuid).offset(skip).limit(limit)
        return db.execute(query).scalars().all()

    def update(self, db: Session, *, db_obj: Event, obj_in: Union[EventUpdate, dict[str, Any]]) -> Event:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, uuid: str) -> Event | None:
        return super().remove(db, id=uuid)
event_crud = CRUDEvent(Event)
