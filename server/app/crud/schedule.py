from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    def get_multi_by_class(
            self, db: Session, *, class_id: int, skip: int = 0, limit: int = 100
    ) -> List[Schedule]:
        return (
            db.query(self.model)
            .filter(Schedule.class_id == class_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


schedule = CRUDSchedule(Schedule)
