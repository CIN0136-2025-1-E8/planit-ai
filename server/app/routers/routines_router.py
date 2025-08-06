from datetime import time

from fastapi import APIRouter, Depends, HTTPException, status, Form, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import get_routine_crud, CRUDRoutine
from app.dependencies import get_db
from app.models import User as UserModel
from app.schemas import RoutineCreateInDB, RoutineUpdate, Routine

routines_router = APIRouter(
    prefix="/routine",
    tags=["Routine"],
)


@routines_router.post(
    path="/",
    response_model=Routine,
    description="""
Creates a new routine.

The `days_of_the_week` field uses bitmasking to represent the days of the week.
Combine the values for the desired days:
- **SUNDAY**: 1
- **MONDAY**: 2
- **TUESDAY**: 4
- **WEDNESDAY**: 8
- **THURSDAY**: 16
- **FRIDAY**: 32
- **SATURDAY**: 64

For example, for a routine on Monday and Wednesday, the value would be 2 + 8 = 10.

Time fields (`start_time`, `end_time`) must be in ISO 8601 time format (e.g., `10:00:00`) and in UTC.
""",
)
def create_routine(
        title: str = Form(),
        description: str | None = Form(None),
        flexible: bool = Form(),
        start_time: str = Form(),
        end_time: str = Form(),
        days_of_the_week: int = Form(),
        routine_crud: CRUDRoutine = Depends(get_routine_crud),
        user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not (1 <= days_of_the_week <= 127):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="days_of_the_week must be an integer between 1 and 127.",
        )

    try:
        _start_time = time.fromisoformat(start_time)
        _end_time = time.fromisoformat(end_time)
        start_time = str(_start_time)
        end_time = str(_end_time)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid ISO 8601 format for start or end time. Use HH:MM:SS.",
        )

    if _end_time <= _start_time:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_time must be after start_time.",
        )

    routine_in: RoutineCreateInDB = RoutineCreateInDB(
        owner_uuid=user.uuid,
        title=title,
        description=description,
        flexible=flexible,
        start_time=start_time,
        end_time=end_time,
        days_of_the_week=days_of_the_week,
    )
    routine = routine_crud.create(db=db, obj_in=routine_in)
    return routine


@routines_router.get(
    path="/list",
    response_model=list[Routine],
    description="Retrieves a list of routines for the current user.",
)
def list_routines(
        skip: int = 0,
        limit: int = 100,
        routine_crud: CRUDRoutine = Depends(get_routine_crud),
        user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    routines = routine_crud.get_routines_by_owner(db, owner_uuid=user.uuid, skip=skip, limit=limit)
    return routines


@routines_router.get(
    path="/",
    response_model=Routine,
    description="Retrieves a specific routine by its UUID.",
)
def get_routine(
        routine_uuid: str = Query(),
        routine_crud: CRUDRoutine = Depends(get_routine_crud),
        user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    routine = routine_crud.get(db, obj_uuid=routine_uuid)
    if not routine or routine.owner_uuid != user.uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return routine


@routines_router.put(
    path="/",
    response_model=Routine,
    description="""
Updates an existing routine.

The `new_days_of_the_week` field uses bitmasking to represent the days of the week.
Combine the values for the desired days:
- **SUNDAY**: 1
- **MONDAY**: 2
- **TUESDAY**: 4
- **WEDNESDAY**: 8
- **THURSDAY**: 16
- **FRIDAY**: 32
- **SATURDAY**: 64

For example, to update a routine to run on Tuesday and Friday, the value would be 4 + 32 = 36.

Time fields (`new_start_time`, `new_end_time`) must be in ISO 8601 time format (e.g., `10:00:00`) and in UTC.
""",
)
def update_routine(
        routine_uuid: str = Form(),
        new_title: str | None = Form(None),
        new_description: str | None = Form(None),
        new_flexible: bool | None = Form(None),
        new_start_time: str | None = Form(None),
        new_end_time: str | None = Form(None),
        new_days_of_the_week: int | None = Form(None),
        routine_crud: CRUDRoutine = Depends(get_routine_crud),
        user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_routine = routine_crud.get(db, obj_uuid=routine_uuid)
    if not db_routine or db_routine.owner_uuid != user.uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if new_days_of_the_week:
        if not (1 <= new_days_of_the_week <= 127):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="new_days_of_the_week must be between 1 and 127.",
            )

    if new_start_time or new_end_time:
        new_start_time = new_start_time if new_start_time else db_routine.start_time
        new_end_time = new_end_time if new_end_time else db_routine.end_time

        try:
            _start_time = time.fromisoformat(new_start_time)
            _end_time = time.fromisoformat(new_end_time)
            new_start_time = str(_start_time)
            new_end_time = str(_end_time)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid ISO 8601 format for start or end time. Use HH:MM:SS.",
            )

        if _end_time <= _start_time:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="end_time must be after start_time."
            )

    routine_update: RoutineUpdate = RoutineUpdate(
        title=new_title,
        description=new_description,
        flexible=new_flexible,
        start_time=new_start_time,
        end_time=new_end_time,
        days_of_the_week=new_days_of_the_week,
    )

    db_routine = routine_crud.get(db, obj_uuid=routine_uuid)
    if not db_routine or db_routine.owner_uuid != user.uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_routine = routine_crud.update(db=db, db_obj=db_routine, obj_in=routine_update)
    return updated_routine


@routines_router.delete(
    path="/",
    response_model=Routine,
    description="Deletes a specific routine by its UUID.",
)
def delete_routine(
        routine_uuid: str = Form(),
        routine_crud: CRUDRoutine = Depends(get_routine_crud),
        user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_routine = routine_crud.get(db, obj_uuid=routine_uuid)
    if not db_routine or db_routine.owner_uuid != user.uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db_routine = routine_crud.remove(db, obj_uuid=routine_uuid)
    if not db_routine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_routine
