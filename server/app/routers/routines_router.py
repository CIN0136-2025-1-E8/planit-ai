from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_db
from app.crud.routine import routine_crud, CRUDRoutine, get_routine_crud
from app.schemas.routine_schema import RoutineCreate, RoutineCreateInDB, RoutineUpdate, Routine
from app.core.security import get_current_user
from app.models import User

routines_router = APIRouter(
    prefix="/routines",
    tags=["Routines"],
)

@routines_router.post("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
def create_new_routine(
    routine_in: RoutineCreate,
    routine_crud: CRUDRoutine = Depends(get_routine_crud),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    routine_create: RoutineCreateInDB = RoutineCreateInDB(**routine_in.model_dump(), owner_uuid=user.uuid)

    routine = routine_crud.create(db=db, obj_in=routine_create)
    return routine


@routines_router.get("/", response_model=list[Routine])
def read_all_routines_by_owner(
    skip: int = 0,
    limit: int = 100,
    routine_crud: CRUDRoutine = Depends(get_routine_crud),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    routines = routine_crud.get_routines_by_owner(db, owner_uuid=user.uuid, skip=skip, limit=limit)
    return routines


@routines_router.get("/{routine_uuid}", response_model=Routine)
def read_routine_by_uuid(
    routine_uuid: str,
    routine_crud: CRUDRoutine = Depends(get_routine_crud),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    routine = routine_crud.get(db, obj_uuid=routine_uuid)
    if routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    if routine.owner_uuid != user.uuid:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this routine."
        )
    return routine


@routines_router.put("/{routine_uuid}", response_model=Routine)
def update_existing_routine(
    routine_uuid: str,
    routine_update: RoutineUpdate,
    routine_crud: CRUDRoutine = Depends(get_routine_crud),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_routine = routine_crud.get(db, obj_uuid=routine_uuid)
    if db_routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    if db_routine.owner_uuid != user.uuid:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this routine."
        )

    updated_routine = routine_crud.update(db=db, db_obj=db_routine, obj_in=routine_update)
    return updated_routine


@routines_router.delete("/{routine_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_routine(
    routine_uuid: str,
    routine_crud: CRUDRoutine = Depends(get_routine_crud),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    routine = routine_crud.remove(db, obj_uuid=routine_uuid)
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )

    return {"message": "Routine deleted successfully"}
