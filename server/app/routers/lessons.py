from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Lesson)
def create_lesson(lesson_in: schemas.LessonCreate, db: Session = Depends(get_db)):
    db_class = crud.class_.get(db, id=lesson_in.class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Turma pai não encontrada")
    return crud.lesson.create(db=db, obj_in=lesson_in)


@router.get("/", response_model=List[schemas.Lesson])
def read_lessons(class_id: int, db: Session = Depends(get_db)):
    return crud.lesson.get_multi_by_class(db, class_id=class_id)


@router.put("/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(lesson_id: int, lesson_in: schemas.LessonUpdate, db: Session = Depends(get_db)):
    db_lesson = crud.lesson.get(db, id=lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    return crud.lesson.update(db=db, db_obj=db_lesson, obj_in=lesson_in)


@router.delete("/{lesson_id}", response_model=schemas.Lesson)
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = crud.lesson.get(db, id=lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    return crud.lesson.remove(db=db, id=lesson_id)
