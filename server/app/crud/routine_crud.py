from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Routine
from app.schemas import RoutineCreateInDB, RoutineUpdate


def get_routine_crud():
    return routine_crud


class CRUDRoutine(CRUDBase[Routine, RoutineCreateInDB, RoutineUpdate]):
    def get_routines_by_owner(self, db: Session, owner_uuid: str, skip: int = 0, limit: int = 100) -> list[Routine]:
        query = (
            select(self.model)
            .filter(self.model.owner_uuid == owner_uuid)
            .offset(skip)
            .limit(limit)
        )
        result = db.execute(query).scalars().all()
        return list(result)


routine_crud = CRUDRoutine(Routine)
