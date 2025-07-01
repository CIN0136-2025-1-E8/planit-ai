from google.genai.types import Content
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


class ChatHistoryRequest(BaseModel):
    session_id: str


class ChatHistory(BaseModel):
    session_id: str
    history: list[Content]
