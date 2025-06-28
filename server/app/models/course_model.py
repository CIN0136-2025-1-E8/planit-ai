import uuid

from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class Course(Base):
    __tablename__ = "courses"

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    semester = Column(String, nullable=True)
    archived = Column(Boolean, default=False, nullable=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)

    owner = relationship("User", back_populates="courses")
    evaluations = relationship("Evaluation", back_populates="course", cascade="all, delete-orphan")
    lectures = relationship("Lecture", back_populates="course", cascade="all, delete-orphan")
