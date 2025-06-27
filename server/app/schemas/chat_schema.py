from enum import Enum

from pydantic import BaseModel


class ChatRoles(Enum):
    USER = "user"
    MODEL = "model"


class ChatPartTypes(Enum):
    TEXT = "text"
    FILE = "file"


class ChatPart(BaseModel):
    type: ChatPartTypes
    content: str


class ChatMessageParts(BaseModel):
    role: ChatRoles
    parts: list[ChatPart]


class ChatResponse(BaseModel):
    session_id: str
    response: str


class ChatHistory(BaseModel):
    session_id: str
    history: list[ChatMessageParts]


class ChatsList(BaseModel):
    session_ids: list[str]
