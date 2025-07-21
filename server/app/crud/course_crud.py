from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud import CRUDBase
from app.models import Course as CourseModel
from app.schemas import Course, CourseCreate, CourseUpdate


def get_course_crud():
    return course_crud


class CRUDCourse(CRUDBase[CourseModel, CourseCreate, CourseUpdate]):
    def create_with_children(self, db: Session, *, obj_in: Course, owner_uuid: str) -> CourseModel:
        from app.models import Evaluation, Lecture
        db_obj = self.model(**obj_in.model_dump(exclude={"evaluations", "lectures"}), owner_uuid=owner_uuid)
        db_obj.evaluations = [Evaluation(**evaluation.model_dump(mode='json'), course_uuid=obj_in.uuid)
                              for evaluation in obj_in.evaluations]
        db_obj.lectures = [Lecture(**lecture.model_dump(), course_uuid=obj_in.uuid)
                           for lecture in obj_in.lectures]
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all_by_owner_uuid(self, db: Session, *, owner_uuid: str) -> list[CourseModel]:
        query = select(self.model).filter(self.model.owner_uuid == owner_uuid)
        result = db.execute(query).scalars().all()
        return list(result)


course_crud = CRUDCourse(CourseModel)
