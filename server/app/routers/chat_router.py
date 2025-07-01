from fastapi import APIRouter, HTTPException
from google import genai
from google.genai.types import Content

from core.config import settings
from crud import chat_crud

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@chat_router.post("/history", response_model=list[Content])
async def get_chat_history():
    chat_history = chat_crud.get_chat_history()
    if not chat_history:
        raise HTTPException(status_code=404, detail="Not Found")
    return chat_crud.get_chat_history()


@chat_router.post("/message", response_model=str)
async def send_chat_message(message: str):
    client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
    chat_history = chat_crud.get_chat_history()
    chat = client.aio.chats.create(model=settings.GOOGLE_BASIC_MODEL, history=chat_history)
    response = await chat.send_message(message)
    chat_crud.set_chat_history(chat.get_history())
    return response.text
