from sqlalchemy.orm import Session
from sqlalchemy import select, asc
import uuid

from app.models import ChatMessage, User
from app.schemas import ChatMessage as ChatMessageSchema, ChatRole

def get_chat_crud():
    return CRUDChat()

class CRUDChat:
    def get_chat_history(self, db: Session, user: User) -> list[ChatMessageSchema]:
        query = (
            select(ChatMessage)
            .where(ChatMessage.owner_uuid == user.uuid)
            .order_by(asc(ChatMessage.order))
        )
        results = db.execute(query).scalars().all()
        return [ChatMessageSchema(role=ChatRole(msg.role), text=msg.content) for msg in results]

    def append_chat_history(self, db: Session, user: User, chat_message: ChatMessageSchema) -> None:
        # Descobre o próximo valor de 'order' para o usuário
        last_order = db.query(ChatMessage.order).filter(ChatMessage.owner_uuid == user.uuid).order_by(ChatMessage.order.desc()).first()
        next_order = (last_order[0] + 1) if last_order else 1
        db_msg = ChatMessage(
            uuid=str(uuid.uuid4()),
            order=next_order,
            role=chat_message.role.value,
            content=chat_message.text,
            owner_uuid=user.uuid
        )
        db.add(db_msg)
        db.commit()

    def delete_chat_history(self, db: Session, user: User) -> None:
        db.query(ChatMessage).filter(ChatMessage.owner_uuid == user.uuid).delete()
        db.commit()

    def remove_message(self, db: Session, user: User, message_uuid: str) -> None:
        db.query(ChatMessage).filter(ChatMessage.owner_uuid == user.uuid, ChatMessage.uuid == message_uuid).delete()
        db.commit()

    def clear_history(self, db: Session, user: User) -> None:
        self.delete_chat_history(db, user)