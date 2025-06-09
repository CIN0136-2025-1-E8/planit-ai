from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.personal_event import PersonalEvent
from app.schemas.personal_event import PersonalEventCreate, PersonalEventUpdate


class CRUDPersonalEvent(CRUDBase[PersonalEvent, PersonalEventCreate, PersonalEventUpdate]):
    def get_multi_by_semester(
            self, db: Session, *, semester_id: int | None = None, skip: int = 0, limit: int = 100
    ) -> List[PersonalEvent]:
        query = db.query(self.model)
        if semester_id:
            query = query.filter(PersonalEvent.semester_id == semester_id)
        return query.offset(skip).limit(limit).all()


personal_event = CRUDPersonalEvent(PersonalEvent)
