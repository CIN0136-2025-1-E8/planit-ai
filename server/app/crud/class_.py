from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.class_ import Class
from app.schemas.class_ import ClassCreate, ClassUpdate


class CRUDClass(CRUDBase[Class, ClassCreate, ClassUpdate]):
    def get_multi_by_semester(
            self, db: Session, *, semester_id: int, skip: int = 0, limit: int = 100
    ) -> List[Class]:
        return (
            db.query(self.model)
            .filter(Class.semester_id == semester_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


class_ = CRUDClass(Class)
