import uuid

from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends
from google.genai.types import Content, Part
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.core.security import get_current_user
from app.crud import get_chat_crud, get_course_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import Course, CourseBase, CourseUpdate, CourseDeleteResponse, Lecture, LectureBase, Evaluation, \
    EvaluationBase
from app.services import get_google_ai_service

course_router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)


@course_router.get("/list")
async def get_courses(
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    return course_crud.get_all_by_owner_uuid(db=db, owner_uuid=current_user.uuid)


@course_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_course(
        files: list[UploadFile],
        message: str | None = Form(None),
        chat_crud=Depends(get_chat_crud),
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    validate_files(files)
    try:
        course: Course = await create_course_iterative(
            files=[(await file.read(), file.content_type) for file in files], message=message)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    system_message = settings.SYSTEM_MESSAGE_MARKER_START + course.model_dump_json() + settings.SYSTEM_MESSAGE_MARKER_END
    created_course = course_crud.create_with_children(db=db, obj_in=course, owner_uuid=current_user.uuid)
    chat_crud.append_llm_context([Content(role="user", parts=[Part(text=system_message)])])
    chat_crud.append_llm_context([Content(role="model", parts=[Part(text="Certo. Lembrarei disso.")])])
    return created_course


@course_router.put("/update", status_code=status.HTTP_200_OK)
async def update_course(
        course_new_data: CourseUpdate,
        course_uuid: str,
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db)):
    course = course_crud.get(db=db, obj_uuid=course_uuid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    updated_course = course_crud.update(db=db, db_obj=course, obj_in=course_new_data)
    return updated_course


@course_router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_course(
        course_uuid: str,
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db)):
    removed_course = course_crud.remove(db=db, obj_uuid=course_uuid)
    response = CourseDeleteResponse.model_validate(removed_course)
    response.deleted_lectures = len(removed_course.lectures)
    response.deleted_evaluations = len(removed_course.evaluations)
    return response


def validate_files(files: list[UploadFile]) -> None:
    files_size = 0
    for file in files:
        if file.content_type not in settings.SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=415, detail="Unsupported Media Type")
        files_size += file.size
        if files_size > 19922944:  # 19MB, leaving 1MB for the rest of the prompt
            raise HTTPException(status_code=413, detail="Request Entity Too Large")


class LecturesCreate(BaseModel):
    lectures: list[LectureBase] = Field(description="The list of lectures parsed from the file in this turn.")
    has_more: bool = Field(description="Whether there are more lectures to be parsed from the file.")


class EvaluationsCreate(BaseModel):
    evaluations: list[EvaluationBase] = Field(description="The list of evaluations parsed from the file in this turn.")
    has_more: bool = Field(description="Whether there are more evaluations to be parsed from the file.")


async def create_course_iterative(files: list[tuple[bytes, str]],
                                  message: str | None = None,
                                  ai_service=get_google_ai_service()) -> Course:
    course_base: CourseBase = await ai_service.generate_structured_output(
        instruction="Fill all fields in Brazillian Portuguese.",
        schema=CourseBase,
        files=files,
        message=message)
    course: Course = Course(uuid=str(uuid.uuid4()), **course_base.model_dump())

    lectures_appended: int = 0
    while True:
        instruction_initial: str = (
            "Parse up to the first ten lectures from the file. Don't confuse lectures with evaluations. Fill all "
            "properties in Brazillian Portuguese if they don't have a format attribute.")
        instruction_iteration: str = (
            f"You have already parsed the first {lectures_appended} lectures from the file, up to "
            f"{course.lectures[-1].start_datetime if course.lectures else None}. Don't confuse lectures with "
            f"evaluations. Parse the next up to ten lectures. Fill all properties in Brazillian Portuguese if they "
            f"don't have a format attribute.")
        lectures: LecturesCreate = await ai_service.generate_structured_output(
            instruction=instruction_iteration if lectures_appended > 0 else instruction_initial,
            schema=LecturesCreate,
            files=files,
            message=message)
        for lecture in lectures.lectures:
            course.lectures.append(Lecture(uuid=str(uuid.uuid4()), **lecture.model_dump()))
            lectures_appended += 1
        if not lectures.has_more:
            break

    evaluations_appended: int = 0
    while True:
        instruction_initial: str = (
            "Parse up to the first ten evaluations from the file. Don't confuse lectures with evaluations. Fill all "
            "properties in Brazillian Portuguese if they don't have a format attribute.")
        instruction_iteration: str = (
            f"You have already parsed the first {evaluations_appended} evaluations from the file, up to "
            f"{course.evaluations[-1].start_datetime if course.evaluations else None}. Don't confuse lectures with "
            f"evaluations. Fill all properties in Brazillian Portuguese if they don't have a format attribute.")
        evaluations: EvaluationsCreate = await ai_service.generate_structured_output(
            instruction=instruction_iteration if evaluations_appended > 0 else instruction_initial,
            schema=EvaluationsCreate,
            files=files,
            message=message)
        for evaluation in evaluations.evaluations:
            course.evaluations.append(Evaluation(uuid=str(uuid.uuid4()), **evaluation.model_dump()))
            evaluations_appended += 1
        if not evaluations.has_more:
            break
    return course
