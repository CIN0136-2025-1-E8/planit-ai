from typing import Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.crud.base import CRUDBase
from app.models.routine_model import Routine
from app.schemas.routine_schema import RoutineCreate, RoutineCreateInDB, RoutineUpdate


def get_routine_crud():
    return routine_crud


class CRUDRoutine(CRUDBase[Routine, RoutineCreateInDB, RoutineUpdate]):
    def create(self, db: Session, *, obj_in: RoutineCreateInDB) -> Routine:
        obj_in_data = obj_in.model_dump()
        
        db_obj = self.model(
            **obj_in_data
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_routine(self, db: Session, uuid: str) -> Routine | None:
        return self.get(db, obj_uuid=uuid)

    def get_routines_by_owner(self, db: Session, owner_uuid: str, skip: int = 0, limit: int = 100) -> list[Routine]:
        query = (
            select(self.model)
            .filter(self.model.owner_uuid == owner_uuid)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(query).scalars().all()

    def update(self, db: Session, *, db_obj: Routine, obj_in: Union[RoutineUpdate, dict[str, Any]]) -> Routine:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, uuid: str) -> Routine | None:
        return self.remove(db, obj_uuid=uuid)

routine_crud = CRUDRoutine(Routine)
