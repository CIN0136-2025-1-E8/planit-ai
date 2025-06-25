from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class CourseFile(Base):
    __tablename__ = "course_files"

    uuid = Column(Integer, primary_key=True, index=True)
    purpose = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    new_name = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    uploaded_at = Column(String, nullable=False)

    course_uuid = Column(Integer, ForeignKey("course.uuid"), nullable=False)
    course = relationship("Course", back_populates="course_files")
