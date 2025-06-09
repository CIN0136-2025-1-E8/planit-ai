from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.PersonalEvent)
def create_personal_event(event_in: schemas.PersonalEventCreate, db: Session = Depends(get_db)):
    if event_in.semester_id:
        db_semester = crud.semester.get(db, id=event_in.semester_id)
        if not db_semester:
            raise HTTPException(status_code=404, detail="Semestre pai não encontrado")
    return crud.personal_event.create(db=db, obj_in=event_in)


@router.get("/", response_model=List[schemas.PersonalEvent])
def read_personal_events(semester_id: int | None = None, db: Session = Depends(get_db)):
    return crud.personal_event.get_multi_by_semester(db=db, semester_id=semester_id)


@router.get("/{event_id}", response_model=schemas.PersonalEvent)
def read_personal_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.personal_event.get(db, id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Evento pessoal não encontrado")
    return db_event


@router.put("/{event_id}", response_model=schemas.PersonalEvent)
def update_personal_event(event_id: int, event_in: schemas.PersonalEventUpdate, db: Session = Depends(get_db)):
    db_event = crud.personal_event.get(db, id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Evento pessoal não encontrado")
    return crud.personal_event.update(db=db, db_obj=db_event, obj_in=event_in)


@router.delete("/{event_id}", response_model=schemas.PersonalEvent)
def delete_personal_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.personal_event.get(db, id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Evento pessoal não encontrado")
    return crud.personal_event.remove(db=db, id=event_id)
