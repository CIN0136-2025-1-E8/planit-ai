from typing import Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import datetime

from app.crud.base import CRUDBase
from app.models import Event
from app.schemas import EventCreateInDB, EventUpdate


def get_event_crud():
    return event_crud


class CRUDEvent(CRUDBase[Event, EventCreateInDB, EventUpdate]):
    def get_events_by_owner(
            self,
            db: Session,
            owner_uuid: str,
            start_utc: datetime | None = None,
            end_utc: datetime | None = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[Event]:
        """Retrieves events for a specific owner within an optional datetime range.

        The method filters events based on their start time. The time range is
        inclusive of the start time and exclusive of the end time.

        Args:
            db (Session): The database session.
            owner_uuid (str): The UUID of the event owner.
            start_utc (datetime | None): The UTC datetime for the start of the
                range (inclusive).
            end_utc (datetime | None): The UTC datetime for the end of the
                range (exclusive).
            skip (int): The number of events to skip for pagination.
            limit (int): The maximum number of events to return.

        Returns:
            list[Event]: A list of Event objects matching the criteria,
                ordered by their start time.
        """
        filters = [self.model.owner_uuid == owner_uuid]
        if start_utc: filters.append(self.model.start_datetime >= start_utc)
        if end_utc: filters.append(self.model.start_datetime < end_utc)

        query = (
            select(self.model)
            .filter(and_(*filters))
            .order_by(self.model.start_datetime)
            .offset(skip)
            .limit(limit)
        )

        results = list(db.execute(query).scalars().all())
        return results

    def update(self, db: Session, *, db_obj: Event, obj_in: Union[EventUpdate, dict[str, Any]]) -> Event:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        # Converta datetime para string ISO 8601 para o modelo do DB (que usa String)
        if 'start_datetime' in update_data and update_data['start_datetime'] is not None:
            update_data['start_datetime'] = update_data['start_datetime'].isoformat()
        if 'end_datetime' in update_data and update_data['end_datetime'] is not None:
            update_data['end_datetime'] = update_data['end_datetime'].isoformat()
        return super().update(db, db_obj=db_obj, obj_in=update_data)


event_crud = CRUDEvent(Event)
