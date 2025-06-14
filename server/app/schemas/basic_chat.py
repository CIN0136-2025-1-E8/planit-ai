from google.genai.types import Content
from pydantic import BaseModel


class BasicChatRequest(BaseModel):
    session_id: str
    message: str


class BasicChatResponse(BaseModel):
    reply: str


class BasicChatHistoryRequest(BaseModel):
    session_id: str


class BasicChatHistory(BaseModel):
    session_id: str
    history: list[Content]
