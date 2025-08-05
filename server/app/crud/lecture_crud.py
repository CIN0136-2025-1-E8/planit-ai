from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.orm import Session, contains_eager

from app.crud.base import CRUDBase
from app.models import Lecture, Course
from app.schemas import LectureCreate, LectureUpdate


def get_lecture_crud():
    return lecture_crud


class CRUDLecture(CRUDBase[Lecture, LectureCreate, LectureUpdate]):
    def get_lectures_by_owner(
            self,
            db: Session,
            owner_uuid: str,
            start_utc: datetime | None = None,
            end_utc: datetime | None = None,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Lecture]:
        filters = [Course.owner_uuid == owner_uuid]
        if start_utc: filters.append(self.model.start_datetime >= start_utc)
        if end_utc: filters.append(self.model.start_datetime < end_utc)

        query = (
            select(self.model)
            .join(Course)
            .options(contains_eager(self.model.course))
            .filter(and_(*filters))
            .order_by(self.model.start_datetime)
            .offset(skip)
            .limit(limit)
        )

        results = list(db.execute(query).scalars().all())
        return results


lecture_crud = CRUDLecture(Lecture)
