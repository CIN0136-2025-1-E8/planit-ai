from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate


class CRUDLesson(CRUDBase[Lesson, LessonCreate, LessonUpdate]):
    def get_multi_by_class(
            self, db: Session, *, class_id: int, skip: int = 0, limit: int = 100
    ) -> List[Lesson]:
        return (
            db.query(self.model)
            .filter(Lesson.class_id == class_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


lesson = CRUDLesson(Lesson)
