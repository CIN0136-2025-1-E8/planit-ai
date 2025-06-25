from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from core.db import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    courses = relationship("Course", back_populates="owner")
    routines = relationship("Routine", back_populates="owner")
    events = relationship("Event", back_populates="owner")
    files = relationship("File", back_populates="owner")
    operation_log = relationship("OperationLog", back_populates="owner")
    chat_history = relationship("ChatHistory", back_populates="owner")
