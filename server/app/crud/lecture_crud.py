from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lecture_model import Lecture
from app.schemas.lecture_schema import LectureCreate, LectureUpdate

def get_lecture_crud():
    return lecture_crud

class CRUDLecture(CRUDBase[Lecture, LectureCreate, LectureUpdate]):
    def get_all_by_course(self, db: Session, *, course_uuid: str) -> list[Lecture]:
        query = select(self.model).filter(self.model.course_uuid == course_uuid)
        result = db.execute(query).scalars().all()
        return list(result)
    
    def get_by_date(self, db: Session, *, day: str) -> list[Lecture]:
        query = select(self.model).filter(self.model.start_datetime.startswith(day)) # analise
        result = db.execute(query).scalars().all()
        return list(result)
    
    def set_presence(self, db: Session, *, uuid: str, present: bool) -> Lecture | None:
        lecture = self.get(db, obj_uuid=uuid)
        if lecture:
            return self.update(db, db_obj=lecture, obj_in={"present": present})
        return None
    

lecture_crud = CRUDLecture(Lecture)