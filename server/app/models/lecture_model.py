import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class Lecture(Base):
    __tablename__ = "lectures"

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=False)
    summary = Column(String, nullable=True)
    present = Column(Boolean, nullable=False, default=False)

    course_uuid = Column(String, ForeignKey("courses.uuid"), index=True, nullable=False)

    course = relationship("Course", back_populates="lectures")
