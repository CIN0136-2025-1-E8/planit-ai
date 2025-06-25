from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class Lecture(Base):
    __tablename__ = "lectures"

    uuid = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_datetime = Column(String, nullable=False)
    end_datetime = Column(String, nullable=False)
    present = Column(Boolean, nullable=False, default=False)

    course_uuid = Column(Integer, ForeignKey("course.uuid"), nullable=False)
    course = relationship("Course", back_populates="lectures")
