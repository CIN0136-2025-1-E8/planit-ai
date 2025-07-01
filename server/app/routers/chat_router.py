from fastapi import APIRouter, HTTPException, BackgroundTasks
from google import genai
from starlette.responses import StreamingResponse

from core.config import settings
from crud import chat_crud
from schemas import ChatResponse, ChatRequest, ChatHistory, ChatHistoryRequest

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@chat_router.post("/history", response_model=ChatHistory)
async def get_chat_history(request: ChatHistoryRequest):
    chat_history = chat_crud.get_chat_history_by_session_id(request.session_id)
    if not chat_history:
        raise HTTPException(status_code=404, detail="Not Found")
    return chat_crud.get_chat_history_by_session_id(request.session_id)


@chat_router.post("/message", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
    chat_history = chat_crud.get_chat_history_by_session_id(request.session_id)
    if chat_history:
        chat = client.aio.chats.create(model=settings.GOOGLE_BASIC_MODEL, history=chat_history.history)
    else:
        chat = client.aio.chats.create(model=settings.GOOGLE_BASIC_MODEL)
    response = await chat.send_message(request.message)
    chat_crud.set_chat_history_by_session_id(
        ChatHistory(session_id=request.session_id, history=chat.get_history()))
    return ChatResponse(reply=response.text)


@chat_router.post("/message_streaming", response_model=ChatResponse)
async def send_chat_message_streaming_response(request: ChatRequest, background_tasks: BackgroundTasks):
    client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
    chat_history = chat_crud.get_chat_history_by_session_id(request.session_id)
    if chat_history:
        chat = client.aio.chats.create(model=settings.GOOGLE_BASIC_MODEL, history=chat_history.history)
    else:
        chat = client.aio.chats.create(model=settings.GOOGLE_BASIC_MODEL)

    def save_chat_history_task():
        chat_crud.set_chat_history_by_session_id(
            ChatHistory(session_id=request.session_id, history=chat.get_history()))

    background_tasks.add_task(save_chat_history_task)

    async def streaming_chat_message():
        async for chunk in await chat.send_message_stream(request.message):
            if chunk.text:
                yield chunk.text

    return StreamingResponse(streaming_chat_message())
