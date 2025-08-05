import uuid

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Course(Base):
    __tablename__ = "courses"

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    semester = Column(String, nullable=True)
    archived = Column(Boolean, default=False, nullable=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), index=True, nullable=False)

    owner = relationship("User", back_populates="courses")
    evaluations = relationship("Evaluation", back_populates="course", cascade="all, delete-orphan")
    lectures = relationship("Lecture", back_populates="course", cascade="all, delete-orphan")
