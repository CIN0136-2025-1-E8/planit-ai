from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class Course(Base):
    __tablename__ = "courses"

    uuid = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    semester = Column(String, nullable=True)
    archived = Column(Boolean, nullable=False, default=False)

    course_files = relationship("CourseFile", back_populates="courses", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="courses", cascade="all, delete-orphan")
    lectures = relationship("Lecture", back_populates="courses", cascade="all, delete-orphan")
