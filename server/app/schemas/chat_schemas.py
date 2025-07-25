from enum import Enum

from pydantic import BaseModel, ConfigDict


class ChatRole(Enum):
    USER = "user"
    MODEL = "model"


class ChatMessageBase(BaseModel):
    role: ChatRole
    text: str


class ChatMessage(ChatMessageBase):
    content: str
    model_config = ConfigDict(from_attributes=True)
