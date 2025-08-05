from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.lecture_schema import Lecture, LectureCreate, LectureUpdate
from app.crud.lecture_crud import get_lecture_crud
from app.core.db import get_db

lecture_router = APIRouter(
    prefix="/lectures",
    tags=["lectures"],
)

@lecture_router.post("/", response_model=Lecture)
def create_lecture(lecture_in: LectureCreate, db: Session = Depends(get_db), crud=Depends(get_lecture_crud)):
    return crud.create(db, obj_in=lecture_in)

@lecture_router.get("/{uuid}", response_model=Lecture)
def get_lecture(uuid: str, db: Session = Depends(get_db), crud=Depends(get_lecture_crud)):
    lecture = crud.get(db, obj_uuid=uuid)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture

@lecture_router.put("/{uuid}", response_model=Lecture)
def update_lecture(uuid: str, lecture_in: LectureUpdate, db: Session = Depends(get_db), crud=Depends(get_lecture_crud)):
    lecture = crud.get(db, obj_uuid=uuid)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return crud.update(db, db_obj=lecture, obj_in=lecture_in)

@lecture_router.delete("/{uuid}", response_model=Lecture)
def delete_lecture(uuid: str, db: Session = Depends(get_db), crud=Depends(get_lecture_crud)):
    lecture = crud.get(db, obj_uuid=uuid)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return crud.remove(db, obj_uuid=uuid)
