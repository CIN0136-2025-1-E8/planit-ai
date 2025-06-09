from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule_in: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_class = crud.class_.get(db, id=schedule_in.class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Turma pai não encontrada")
    return crud.schedule.create(db=db, obj_in=schedule_in)


@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(class_id: int, db: Session = Depends(get_db)):
    return crud.schedule.get_multi_by_class(db, class_id=class_id)


@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule_in: schemas.ScheduleUpdate, db: Session = Depends(get_db)):
    db_schedule = crud.schedule.get(db, id=schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return crud.schedule.update(db=db, db_obj=db_schedule, obj_in=schedule_in)


@router.delete("/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = crud.schedule.get(db, id=schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return crud.schedule.remove(db=db, id=schedule_id)
