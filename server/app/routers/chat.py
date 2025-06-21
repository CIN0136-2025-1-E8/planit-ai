import json
import uuid

from fastapi import APIRouter, BackgroundTasks, Form, HTTPException
from starlette.responses import StreamingResponse

from core.config import settings
from crud import chat_crud
from schemas import ChatRoles, ChatPartTypes, ChatPart, ChatMessageParts, ChatResponse, ChatHistory, ChatsList
from services.google_ai_service import google_ai_service
from utils.file_handling import validate_filenames

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={400: {"description": "Bad Request"},
               404: {"description": "Not found"}},
)


@chat_router.get(path="/list", response_model=ChatsList)
async def get_chats_list():
    chat_list: list[str] = chat_crud.get_user_chats_list()
    if not chat_list:
        raise HTTPException(status_code=404, detail="Not found")
    return chat_list


@chat_router.get("/history", response_model=ChatHistory)
async def get_chat_history(session_id: str):
    chat_history = chat_crud.get_chat_history_by_session_id(session_id)
    if not chat_history:
        raise HTTPException(status_code=404, detail="Not Found")
    return chat_history


@chat_router.post("/message/", response_model=ChatResponse)
async def send_chat_message(session_id: str = Form(None),
                            filenames: list[str] = Form(None),
                            message: str = Form(None)):
    if not filenames and (not message or message == ""):
        raise HTTPException(status_code=400, detail="Bad Request")
    if filenames: validate_filenames(filenames)

    chat_history = chat_crud.get_chat_history_by_session_id(session_id)
    if chat_history is None: session_id = create_session_id()

    user_message_parts: ChatMessageParts = create_user_message_parts(filenames=filenames, message=message)

    response = await google_ai_service.send_message(model=settings.GOOGLE_ADVANCED_MODEL,
                                                    message=user_message_parts,
                                                    chat_history=chat_history)

    model_message_parts: ChatMessageParts = create_model_message_parts(response=response)
    chat_crud.append_to_history_by_session_id(session_id=session_id, part=user_message_parts)
    chat_crud.append_to_history_by_session_id(session_id=session_id, part=model_message_parts)

    return ChatResponse(session_id=session_id, response=response)


@chat_router.post("/message/stream_response")
async def send_chat_message_stream_response(background_tasks: BackgroundTasks,
                                            session_id: str = Form(None),
                                            filenames: list[str] = Form(None),
                                            message: str = Form(None), ):
    if not filenames and (not message or message == ""):
        raise HTTPException(status_code=400, detail="Bad Request")
    if filenames: validate_filenames(filenames)

    chat_history = chat_crud.get_chat_history_by_session_id(session_id)
    if chat_history is None: session_id = create_session_id()

    user_message_parts: ChatMessageParts = create_user_message_parts(filenames=filenames, message=message)

    async def message_stream(chunks: list[str]):
        yield f"event: metadata\ndata: {json.dumps({'session_id': session_id})}\n\n"
        async for chunk in await google_ai_service.send_message_stream_response(model=settings.GOOGLE_ADVANCED_MODEL,
                                                                                message=user_message_parts,
                                                                                chat_history=chat_history):
            if chunk:
                chunks.append(chunk)
                yield f"event: message_chunk\ndata: {json.dumps({'token': chunk}, ensure_ascii=False)}\n\n"
        yield f"event: end\ndata: Stream finished\n\n"

    def append_to_history_task(session_id: str, chunks: list[str]) -> None:
        response: str = "".join(chunks)
        model_message_parts: ChatMessageParts = create_model_message_parts(response=response)
        chat_crud.append_to_history_by_session_id(session_id=session_id, part=user_message_parts)
        chat_crud.append_to_history_by_session_id(session_id=session_id, part=model_message_parts)

    response_chunks: list[str] = []
    background_tasks.add_task(append_to_history_task, session_id=session_id, chunks=response_chunks)

    return StreamingResponse(message_stream(response_chunks), media_type="text/event-stream")


def create_session_id() -> str:
    return str(uuid.uuid4())


def create_user_message_parts(filenames: list[str] | None, message: str | None) -> ChatMessageParts | None:
    message_parts: ChatMessageParts = ChatMessageParts(role=ChatRoles.USER.value, parts=[])
    if filenames:
        for filename in filenames:
            message_parts.parts.append(ChatPart(type=ChatPartTypes.FILE.value,
                                                content=filename))
    if message and message != "":
        message_parts.parts.append(ChatPart(type=ChatPartTypes.TEXT.value,
                                            content=message))
    if message_parts.parts:
        return message_parts
    return None


def create_model_message_parts(response: str) -> ChatMessageParts:
    return ChatMessageParts(role=ChatRoles.MODEL.value,
                            parts=[ChatPart(
                                type=ChatPartTypes.TEXT.value,
                                content=response)])
