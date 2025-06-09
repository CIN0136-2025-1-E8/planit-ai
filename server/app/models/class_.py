from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    class_title = Column(String, nullable=False)
    class_code = Column(String, nullable=True)
    professor_name = Column(String, nullable=True)

    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    semester = relationship("Semester", back_populates="classes")


    schedules = relationship("Schedule", back_populates="class_", cascade="all, delete-orphan")
    lessons = relationship("Lesson", back_populates="class_", cascade="all, delete-orphan")
    overrides = relationship("ScheduleOverride", back_populates="class_", cascade="all, delete-orphan")
