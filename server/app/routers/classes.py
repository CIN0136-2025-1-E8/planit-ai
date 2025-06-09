from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Class)
def create_class(class_in: schemas.ClassCreate, db: Session = Depends(get_db)):
    db_semester = crud.semester.get(db, id=class_in.semester_id)
    if not db_semester:
        raise HTTPException(status_code=404, detail="Semestre pai não encontrado")
    return crud.class_.create(db=db, obj_in=class_in)


@router.get("/", response_model=List[schemas.Class])
def read_classes(semester_id: int, db: Session = Depends(get_db)):
    return crud.class_.get_multi_by_semester(db=db, semester_id=semester_id)


@router.get("/{class_id}", response_model=schemas.ClassWithDetails)
def read_class(class_id: int, db: Session = Depends(get_db)):
    db_class = crud.class_.get(db, id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return db_class


@router.put("/{class_id}", response_model=schemas.Class)
def update_class(class_id: int, class_in: schemas.ClassUpdate, db: Session = Depends(get_db)):
    db_class = crud.class_.get(db, id=class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return crud.class_.update(db=db, db_obj=db_class, obj_in=class_in)


@router.delete("/{class_id}", response_model=schemas.Class)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    db_class = crud.class_.get(db, id=class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return crud.class_.remove(db=db, id=class_id)
