import uuid

from sqlalchemy import Column, String, Integer, Text, ForeignKey, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    order = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    owner_uuid = Column(Integer, ForeignKey("users.uuid"))

    owner = relationship("User", back_populates="chat_history")
