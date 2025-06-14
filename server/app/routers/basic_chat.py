from fastapi import APIRouter, HTTPException
from google import genai

from core.config import settings
from crud import basic_chat_crud
from schemas import BasicChatResponse, BasicChatRequest, BasicChatHistory, BasicChatHistoryRequest

basic_chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@basic_chat_router.post("/history", response_model=BasicChatHistory)
async def basic_chat_get_history(request: BasicChatHistoryRequest):
    chat_history = basic_chat_crud.get_chat_history_by_session_id(request.session_id)
    if not chat_history:
        raise HTTPException(status_code=404, detail="Not Found")
    return basic_chat_crud.get_chat_history_by_session_id(request.session_id)


@basic_chat_router.post("/message", response_model=BasicChatResponse)
async def basic_chat_message(request: BasicChatRequest):
    client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
    chat_history = basic_chat_crud.get_chat_history_by_session_id(request.session_id)
    if chat_history:
        chat = client.aio.chats.create(model=settings.GOOGLE_MODEL_BASIC, history=chat_history.history)
    else:
        chat = client.aio.chats.create(model=settings.GOOGLE_MODEL_BASIC)
    response = await chat.send_message(request.message)
    basic_chat_crud.write_chat_history_by_session_id(
        BasicChatHistory(session_id=request.session_id, history=chat.get_history()))
    return BasicChatResponse(reply=response.text)
