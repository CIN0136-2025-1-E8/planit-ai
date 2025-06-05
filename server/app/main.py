import os
import pickle

import uvicorn
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai.types import Content
from pydantic import BaseModel

from core.config import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY.get_secret_value())
model = settings.GOOGLE_MODEL

app = FastAPI()


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


class HistoryRequest(BaseModel):
    session_id: str


class ChatHistory(BaseModel):
    session_id: str
    history: list[Content]


history = {}
if os.path.exists(settings.DEBUG_HISTORY_FILE_PATH):
    with open(settings.DEBUG_HISTORY_FILE_PATH, 'rb') as file:
        history = pickle.load(file)


@app.post("/chat/message", response_model=ChatResponse)
async def chat_send_message(request: ChatRequest):
    if request.session_id not in history:
        history[request.session_id] = []
    chat = client.aio.chats.create(model=model, history=history[request.session_id])
    response = await chat.send_message(request.message)
    history[request.session_id] = chat.get_history()
    with open(settings.DEBUG_HISTORY_FILE_PATH, "wb") as f:
        pickle.dump(history, f)
    return ChatResponse(reply=response.text)


@app.post("/chat/history", response_model=ChatHistory)
async def chat_get_history(request: HistoryRequest):
    if request.session_id not in history:
        raise HTTPException(status_code=404, detail="Not Found")
    return ChatHistory(session_id=request.session_id, history=history[request.session_id])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
