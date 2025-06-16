import json
from typing import Annotated

from fastapi import APIRouter, HTTPException, Form, UploadFile
from google import genai
from google.genai import types

from core.config import settings
from crud import rich_chat_crud
from schemas import BasicChatHistory, BasicChatHistoryRequest
from schemas.json_definitions import SCHEMA_REGISTRY, AvailableSchemas

rich_chat_router = APIRouter(
    prefix="/chat/rich",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

supported_file_types = ["application/pdf",
                        "application/x-javascript",
                        "text/javascript",
                        "application/x-python",
                        "text/x-python",
                        "text/plain",
                        "text/html",
                        "text/css",
                        "text/md",
                        "text/csv",
                        "text/xml",
                        "text/rtf",
                        "image/png",
                        "image/jpeg",
                        "image/webp",
                        "image/heic",
                        "image/heif"]


@rich_chat_router.post("/history", response_model=BasicChatHistory)
async def rich_chat_get_history(request: BasicChatHistoryRequest):
    chat_history = rich_chat_crud.get_chat_history_by_session_id(request.session_id)
    if not chat_history:
        raise HTTPException(status_code=404, detail="Not Found")
    return chat_history


@rich_chat_router.post("/message/")
async def rich_chat_message(
        session_id: Annotated[str, Form()],
        message: Annotated[str | None, Form()] = None,
        files: list[UploadFile] | None = None,
):
    if files:
        files_size = 0
        for file in files:
            if file.content_type not in supported_file_types:
                raise HTTPException(status_code=415, detail="Unsupported Media Type")
            files_size += file.size
            if files_size > 19922944:  # 19MB, leaving 1MB for prompts and files previously uploaded
                raise HTTPException(status_code=413, detail="Request Entity Too Large")

    client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
    chat_history = rich_chat_crud.get_chat_history_by_session_id(session_id)

    parts = []
    if files:
        for file in files:
            parts.append(types.Part.from_bytes(
                data=file.file.read(),
                mime_type=file.content_type,
            ))
    if message:
        parts.append(message)

    if chat_history:
        chat = client.aio.chats.create(model=settings.GOOGLE_ADVANCED_MODEL, history=chat_history.history)
    else:
        chat = client.aio.chats.create(model=settings.GOOGLE_ADVANCED_MODEL)

    response = await chat.send_message(
        parts,
        types.GenerateContentConfig(system_instruction=settings.LLM_SYSTEM_INSTRUCTIONS_STRUCTURED)
    )

    rich_chat_crud.set_chat_history_by_session_id(
        BasicChatHistory(session_id=session_id, history=chat.get_history()))

    return response.text


@rich_chat_router.post("/message/structured")
async def rich_chat_message_structured(
        session_id: Annotated[str, Form()],
        response_schema: AvailableSchemas = AvailableSchemas.CLASS,
        message: Annotated[str | None, Form()] = None,
        files: list[UploadFile] | None = None,
):
    if files:
        files_size = 0
        for file in files:
            if file.content_type not in supported_file_types:
                raise HTTPException(status_code=415, detail="Unsupported Media Type")
            files_size += file.size
            if files_size > 19922944:  # 19MB, leaving 1MB for prompts and files previously uploaded
                raise HTTPException(status_code=413, detail="Request Entity Too Large")

    client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
    chat_history = rich_chat_crud.get_chat_history_by_session_id(session_id)

    parts = []
    if files:
        for file in files:
            parts.append(types.Part.from_bytes(
                data=file.file.read(),
                mime_type=file.content_type,
            ))
    if message:
        parts.append(message)

    if chat_history:
        chat = client.aio.chats.create(model=settings.GOOGLE_ADVANCED_MODEL, history=chat_history.history)
    else:
        chat = client.aio.chats.create(model=settings.GOOGLE_ADVANCED_MODEL)

    response = await chat.send_message(
        parts,
        types.GenerateContentConfig(
            system_instruction=settings.LLM_STRUCTURED_OUTPUT_SYSTEM_INSTRUCTIONS.get(response_schema),
            response_mime_type="application/json",
            response_schema=SCHEMA_REGISTRY[response_schema],
        )
    )

    rich_chat_crud.set_chat_history_by_session_id(
        BasicChatHistory(session_id=session_id, history=chat.get_history()))

    return json.loads(response.text)
