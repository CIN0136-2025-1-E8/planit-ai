import os
import pickle

from fastapi import APIRouter, HTTPException
from google import genai

from core.config import settings
from schemas import ChatResponse, ChatRequest, ChatHistory, HistoryRequest

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
model = settings.GOOGLE_MODEL

history = {}
if os.path.exists(settings.DEBUG_HISTORY_FILE_PATH):
    with open(settings.DEBUG_HISTORY_FILE_PATH, 'rb') as file:
        history = pickle.load(file)


@router.post("/chat/message", response_model=ChatResponse)
async def chat_send_message(request: ChatRequest):
    if request.session_id not in history:
        history[request.session_id] = []
    chat = client.aio.chats.create(model=model, history=history[request.session_id])
    response = await chat.send_message(request.message)
    history[request.session_id] = chat.get_history()
    with open(settings.DEBUG_HISTORY_FILE_PATH, "wb") as f:
        # noinspection PyTypeChecker
        pickle.dump(history, f)
    return ChatResponse(reply=response.text)


@router.post("/chat/history", response_model=ChatHistory)
async def chat_get_history(request: HistoryRequest):
    if request.session_id not in history:
        raise HTTPException(status_code=404, detail="Not Found")
    return ChatHistory(session_id=request.session_id, history=history[request.session_id])
