import json
import uuid
from typing import Type, TypeVar

from sqlalchemy.orm import Session

from app.core.db import Base
from app.models import ChatMessage, User
from app.schemas import ChatMessage as ChatMessageSchema

ModelType = TypeVar("ModelType", bound=Base)


def get_chat_crud():
    return chat_crud


class CRUDChat:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # noinspection PyMethodMayBeStatic
    def get_chat_history(self, db: Session, user_uuid: str) -> list[ChatMessage]:
        user = db.get(User, user_uuid)
        return user.chat_history

    def append_chat_history(self, db: Session, user_uuid: str, obj_in: ChatMessageSchema) -> None:
        user = db.get(User, user_uuid)
        next_order = len(user.chat_history)

        obj_in_data = obj_in.model_dump(mode='json')
        if 'files' in obj_in_data and obj_in_data['files'] is not None:
            obj_in_data['files'] = json.dumps(obj_in_data['files'])

        db_msg = self.model(
            **obj_in_data,
            uuid=str(uuid.uuid4()),
            order=next_order,
            owner_uuid=user.uuid
        )
        db.add(db_msg)
        db.commit()

    def delete_chat_history(self, db: Session, user_uuid: str) -> int:
        num_deleted = db.query(self.model).filter_by(owner_uuid=user_uuid).delete()
        db.commit()
        return num_deleted


chat_crud = CRUDChat(ChatMessage)
