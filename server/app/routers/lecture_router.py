from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import get_current_user
from app.crud import get_lecture_crud, get_course_crud, CRUDLecture, CRUDCourse
from app.dependencies import get_db
from app.models import User as UserModel, Course as CourseModel, Lecture as LectureModel
from app.schemas import Lecture, LectureCreate, LectureUpdate

lecture_router = APIRouter(
    prefix="/lecture",
    tags=["Lecture"],
)


@lecture_router.get("/", response_model=Lecture)
def get_lecture(
        lecture_uuid: str = Query(),
        db: Session = Depends(get_db),
        course_crud: CRUDCourse = Depends(get_course_crud),
        lecture_crud: CRUDLecture = Depends(get_lecture_crud),
        user: UserModel = Depends(get_current_user),
):
    db_lecture = _validate_authorization_lecture(
        lecture_uuid=lecture_uuid,
        db=db,
        user=user,
        course_crud=course_crud,
        lecture_crud=lecture_crud,
    )
    lecture: Lecture = Lecture.model_validate(db_lecture)
    return lecture


@lecture_router.put("/", response_model=Lecture)
def update_lecture(
        lecture_uuid: str = Form(),
        new_title: str | None = Form(None),
        new_start_datetime: datetime | None = Form(None),
        new_end_datetime: datetime | None = Form(None),
        new_summary: str | None = Form(None),
        new_present: bool | None = Form(None),
        db: Session = Depends(get_db),
        course_crud: CRUDCourse = Depends(get_course_crud),
        lecture_crud: CRUDLecture = Depends(get_lecture_crud),
        user: UserModel = Depends(get_current_user),
):
    db_lecture = _validate_authorization_lecture(
        lecture_uuid=lecture_uuid,
        db=db,
        user=user,
        course_crud=course_crud,
        lecture_crud=lecture_crud,
    )
    lecture_update: LectureUpdate = LectureUpdate(
        title=new_title,
        start_datetime=new_start_datetime,
        end_datetime=new_end_datetime,
        summary=new_summary,
        present=new_present,
    )
    updated_db_lecture: LectureModel = lecture_crud.update(db=db, db_obj=db_lecture, obj_in=lecture_update)
    updated_lecture: Lecture = Lecture.model_validate(updated_db_lecture)
    return updated_lecture


@lecture_router.post("/", response_model=Lecture)
def create_lecture(
        title: str = Form(),
        start_datetime: datetime = Form(),
        end_datetime: datetime = Form(),
        summary: str | None = Form(None),
        course_uuid: str = Form(),
        db: Session = Depends(get_db),
        course_crud: CRUDCourse = Depends(get_course_crud),
        lecture_crud: CRUDLecture = Depends(get_lecture_crud),
        user: UserModel = Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_course: CourseModel = course_crud.get(db=db, obj_uuid=course_uuid)
    if not db_course or db_course.owner_uuid != user.uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    lecture: LectureCreate = LectureCreate(
        title=title,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        summary=summary,
        course_uuid=course_uuid,
    )
    db_lecture: LectureModel = lecture_crud.create(db=db, obj_in=lecture)
    created_lecture: Lecture = Lecture.model_validate(db_lecture)
    return created_lecture


@lecture_router.delete("/", response_model=Lecture)
def delete_lecture(
        lecture_uuid: str = Form(),
        db: Session = Depends(get_db),
        course_crud: CRUDCourse = Depends(get_course_crud),
        lecture_crud: CRUDLecture = Depends(get_lecture_crud),
        user: UserModel = Depends(get_current_user),
):
    db_lecture = _validate_authorization_lecture(
        lecture_uuid=lecture_uuid,
        db=db,
        user=user,
        course_crud=course_crud,
        lecture_crud=lecture_crud,
    )
    db_lecture = lecture_crud.remove(db=db, obj_uuid=db_lecture.uuid)
    deleted_lecture: Lecture = Lecture.model_validate(db_lecture)
    return deleted_lecture


def _validate_authorization_lecture(
        lecture_uuid: str,
        db: Session,
        user: UserModel,
        course_crud: CRUDCourse,
        lecture_crud: CRUDLecture,
) -> LectureModel:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_lecture: LectureModel = lecture_crud.get(db=db, obj_uuid=lecture_uuid)
    if not db_lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_course: CourseModel = course_crud.get(db=db, obj_uuid=db_lecture.course_uuid)
    if not db_course or db_course.owner_uuid != user.uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_lecture
