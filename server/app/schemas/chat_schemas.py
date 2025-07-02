from enum import Enum

from pydantic import BaseModel


class ChatRole(Enum):
    USER = "user"
    MODEL = "model"


class ChatMessage(BaseModel):
    role: ChatRole
    text: str
