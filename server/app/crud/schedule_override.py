from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.schedule_override import ScheduleOverride
from app.schemas.schedule_override import ScheduleOverrideCreate, ScheduleOverrideUpdate


class CRUDScheduleOverride(CRUDBase[ScheduleOverride, ScheduleOverrideCreate, ScheduleOverrideUpdate]):
    def get_multi_by_class(
            self, db: Session, *, class_id: int, skip: int = 0, limit: int = 100
    ) -> List[ScheduleOverride]:
        return (
            db.query(self.model)
            .filter(ScheduleOverride.class_id == class_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


schedule_override = CRUDScheduleOverride(ScheduleOverride)
