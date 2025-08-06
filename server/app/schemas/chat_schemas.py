import json
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class ChatRole(Enum):
    USER = "user"
    MODEL = "model"


class ChatFile(BaseModel):
    filename: str
    mimetype: str


class ChatMessageBase(BaseModel):
    role: ChatRole
    text: str
    files: list[ChatFile] | None = None

    @field_validator('files', mode='before')
    @classmethod
    def parse_files_json(cls, v):
        """
        When loading from the DB, 'files' is a JSON string.
        This validator parses it into a Python list before other validation.
        """
        if isinstance(v, str):
            return json.loads(v)
        return v


class ChatMessage(ChatMessageBase):
    content: str
    model_config = ConfigDict(from_attributes=True)
