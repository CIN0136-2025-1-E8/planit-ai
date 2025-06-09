from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Semester)
def create_semester(semester_in: schemas.SemesterCreate, db: Session = Depends(get_db)):
    return crud.semester.create(db=db, obj_in=semester_in)


@router.get("/", response_model=List[schemas.Semester])
def read_semesters(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.semester.get_multi(db, skip=skip, limit=limit)


@router.get("/{semester_id}", response_model=schemas.SemesterWithDetails)
def read_semester(semester_id: int, db: Session = Depends(get_db)):
    db_semester = crud.semester.get(db, id=semester_id)
    if db_semester is None:
        raise HTTPException(status_code=404, detail="Semestre não encontrado")
    return db_semester


@router.put("/{semester_id}", response_model=schemas.Semester)
def update_semester(
        semester_id: int, semester_in: schemas.SemesterUpdate, db: Session = Depends(get_db)
):
    db_semester = crud.semester.get(db, id=semester_id)
    if not db_semester:
        raise HTTPException(status_code=404, detail="Semestre não encontrado")
    return crud.semester.update(db=db, db_obj=db_semester, obj_in=semester_in)


@router.delete("/{semester_id}", response_model=schemas.Semester)
def delete_semester(semester_id: int, db: Session = Depends(get_db)):
    db_semester = crud.semester.get(db, id=semester_id)
    if not db_semester:
        raise HTTPException(status_code=404, detail="Semestre não encontrado")
    return crud.semester.remove(db=db, id=semester_id)
