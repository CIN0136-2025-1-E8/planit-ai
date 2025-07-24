import uuid

from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends
from google.genai.types import Content, Part
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.core.security import get_current_user
from app.crud import get_chat_crud, get_course_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import Course, CourseUpdate, CourseGenerate, CourseDeleteResponse, Lecture, Evaluation
from app.services import get_google_ai_service, GoogleAIService

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
        current_user: User = Depends(get_current_user),
        ai_service: GoogleAIService = Depends(get_google_ai_service)):
    validate_files(files)
    try:
        course_generated = await ai_service.generate_structured_output(
            files=[(await file.read(), file.content_type) for file in files],
            schema=CourseGenerate,
            message=message,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while parsing course information"
        )

    system_message = settings.SYSTEM_MESSAGE_MARKER_START + course_generated.model_dump_json() + settings.SYSTEM_MESSAGE_MARKER_END
    course: Course = Course(
        uuid=str(uuid.uuid4()),
        title=course_generated.title,
        semester=course_generated.semester,
        lectures=[Lecture(**lecture.model_dump(), uuid=str(uuid.uuid4()))
                  for lecture in course_generated.lectures],
        evaluations=[Evaluation(**{**evaluation.model_dump(), "type": evaluation.type.value}, uuid=str(uuid.uuid4()))
                     for evaluation in course_generated.evaluations]
    )
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
