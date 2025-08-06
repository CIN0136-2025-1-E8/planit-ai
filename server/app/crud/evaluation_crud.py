from datetime import datetime
from typing import Union, Any

from sqlalchemy import select, and_
from sqlalchemy.orm import Session, contains_eager

from app.crud.base import CRUDBase
from app.models import Evaluation, Course
from app.schemas import EvaluationCreate, EvaluationUpdate, EvaluationTypes


def get_evaluation_crud():
    return evaluation_crud


class CRUDEvaluation(CRUDBase[Evaluation, EvaluationCreate, EvaluationUpdate]):
    def get_evaluations_by_owner(
            self,
            db: Session,
            owner_uuid: str,
            start_utc: datetime | None = None,
            end_utc: datetime | None = None,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Evaluation]:
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

    def create(self, db: Session, *, obj_in: EvaluationCreate) -> Evaluation:
        """
        Overrides the base create method to handle the EvaluationTypes enum.
        """
        obj_in_data = obj_in.model_dump()
        if isinstance(obj_in_data.get("type"), EvaluationTypes):
            obj_in_data["type"] = obj_in_data["type"].value

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Evaluation, obj_in: Union[EvaluationUpdate, dict[str, Any]]) -> Evaluation:
        """
        Overrides the base update method to handle the EvaluationTypes enum.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "type" in update_data and isinstance(update_data.get("type"), EvaluationTypes):
            update_data["type"] = update_data["type"].value

        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


evaluation_crud = CRUDEvaluation(Evaluation)
