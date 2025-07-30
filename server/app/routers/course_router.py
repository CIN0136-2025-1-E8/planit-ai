import json
import uuid
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends
from google.genai.types import Content, Part
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.core.security import get_current_user
from app.crud import get_chat_crud, get_course_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import Course, CourseUpdate, CourseGenerate, CourseDeleteResponse, Lecture, Evaluation, ChatMessage, \
    ChatRole
from app.services import get_google_ai_service, GoogleAIService
from app.utils.time import to_utc_iso

course_router = APIRouter(
    prefix="/course",
    tags=["Course"],
    responses={404: {"description": "Not found"}},
)


@course_router.get("/list")
async def list_courses(
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return course_crud.get_all_by_owner_uuid(db=db, owner_uuid=current_user.uuid)


@course_router.post("/ai")
async def create_course_ai(
        files: list[UploadFile],
        message: str | None = Form(None),
        timezone: str | None = Form(None),
        chat_crud=Depends(get_chat_crud),
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        ai_service: GoogleAIService = Depends(get_google_ai_service),
):
    validate_files(files)
    try:
        if timezone: ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid timezone identifier: '{timezone}'"
        )

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

    if timezone:
        client_tz = ZoneInfo(timezone)
        for lecture in course_generated.lectures:
            lecture.start_datetime = to_utc_iso(lecture.start_datetime, client_tz)
            lecture.end_datetime = to_utc_iso(lecture.end_datetime, client_tz)
        for evaluation in course_generated.evaluations:
            evaluation.start_datetime = to_utc_iso(evaluation.start_datetime, client_tz)
            evaluation.end_datetime = to_utc_iso(evaluation.end_datetime, client_tz)

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
    user_message: ChatMessage = ChatMessage(
        role=ChatRole.USER,
        text=f"\"{created_course.title}\" adicionado.",
        content=json.dumps([Content(role="user", parts=[Part(text=system_message)]).model_dump()])
    )
    model_response: str = "Certo. Lembrarei disso."
    model_message: ChatMessage = ChatMessage(
        role=ChatRole.MODEL,
        text=model_response,
        content=json.dumps([Content(role="model", parts=[Part(text=model_response)]).model_dump()])
    )
    chat_crud.append_chat_history(db=db, user_uuid=current_user.uuid, obj_in=user_message)
    chat_crud.append_chat_history(db=db, user_uuid=current_user.uuid, obj_in=model_message)
    return created_course


@course_router.put("/")
async def update_course(
        course_uuid: str = Form(),
        new_title: str | None = Form(None),
        new_semester: str | None = Form(None),
        new_archived: bool | None = Form(None),
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db),
):
    course_new_data = CourseUpdate(
        title=new_title,
        semester=new_semester,
        archived=new_archived,
    )
    course = course_crud.get(db=db, obj_uuid=course_uuid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    updated_course = course_crud.update(db=db, db_obj=course, obj_in=course_new_data)
    return updated_course


@course_router.delete("/")
async def delete_course(
        course_uuid: str = Form(),
        course_crud=Depends(get_course_crud),
        db: Session = Depends(get_db),
):
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
