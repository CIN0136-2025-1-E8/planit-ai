import uuid

from sqlalchemy import Boolean, Column, String, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    courses = relationship("Course", back_populates="owner")
    routines = relationship("Routine", back_populates="owner")
    events = relationship("Event", back_populates="owner")
    files = relationship("File", back_populates="owner")
    operation_log = relationship("Operation", order_by="Operation.order", back_populates="owner")
    chat_history = relationship("ChatMessage", order_by="ChatMessage.order", back_populates="owner")
