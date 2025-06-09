from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ScheduleOverride)
def create_schedule_override(override_in: schemas.ScheduleOverrideCreate, db: Session = Depends(get_db)):
    db_class = crud.class_.get(db, id=override_in.class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Turma pai não encontrada")
    return crud.schedule_override.create(db=db, obj_in=override_in)


@router.get("/", response_model=List[schemas.ScheduleOverride])
def read_schedule_overrides(class_id: int, db: Session = Depends(get_db)):
    return crud.schedule_override.get_multi_by_class(db, class_id=class_id)


@router.put("/{override_id}", response_model=schemas.ScheduleOverride)
def update_schedule_override(override_id: int, override_in: schemas.ScheduleOverrideUpdate,
                             db: Session = Depends(get_db)):
    db_override = crud.schedule_override.get(db, id=override_id)
    if not db_override:
        raise HTTPException(status_code=404, detail="Exceção de horário não encontrada")
    return crud.schedule_override.update(db=db, db_obj=db_override, obj_in=override_in)


@router.delete("/{override_id}", response_model=schemas.ScheduleOverride)
def delete_schedule_override(override_id: int, db: Session = Depends(get_db)):
    db_override = crud.schedule_override.get(db, id=override_id)
    if not db_override:
        raise HTTPException(status_code=404, detail="Exceção de horário não encontrada")
    return crud.schedule_override.remove(db=db, id=override_id)
