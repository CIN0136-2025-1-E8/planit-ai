import uuid

from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends
from google.genai.types import Content, Part
from starlette import status

from core.config import settings
from crud import get_chat_crud, get_course_crud
from schemas import Course, CourseBase
from services import get_google_ai_service

course_router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)


@course_router.get("/list", response_model=list[Course])
async def get_courses(course_crud=Depends(get_course_crud)):
    return course_crud.get_courses()


@course_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_course(
        files: list[UploadFile],
        message: str | None = Form(None),
        chat_crud=Depends(get_chat_crud),
        course_crud=Depends(get_course_crud),
        ai_service=Depends(get_google_ai_service)):
    validate_files(files)
    try:
        course_base: CourseBase = await ai_service.generate_structured_output(
            instruction=None,
            schema=CourseBase,
            files=[[await file.read(), file.content_type] for file in files],
            message=message)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    course: Course = Course(uuid=str(uuid.uuid4()), **course_base.model_dump())
    system_message = settings.SYSTEM_MESSAGE_MARKER_START + course_base.model_dump_json() + settings.SYSTEM_MESSAGE_MARKER_END
    course_crud.append_course(course)
    chat_crud.append_llm_context([Content(role="user", parts=[Part(text=system_message)])])
    chat_crud.append_llm_context([Content(role="model", parts=[Part(text="Certo. Lembrarei disso.")])])


def validate_files(files: list[UploadFile]) -> None:
    files_size = 0
    for file in files:
        if file.content_type not in settings.SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=415, detail="Unsupported Media Type")
        files_size += file.size
        if files_size > 19922944:  # 19MB, leaving 1MB for the rest of the prompt
            raise HTTPException(status_code=413, detail="Request Entity Too Large")
