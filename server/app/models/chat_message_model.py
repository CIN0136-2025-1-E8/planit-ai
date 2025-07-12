from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    uuid = Column(String, primary_key=True)
    order = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    owner_uuid = Column(Integer, ForeignKey("users.uuid"), index=True, nullable=False)

    owner = relationship("User", back_populates="chat_history")
