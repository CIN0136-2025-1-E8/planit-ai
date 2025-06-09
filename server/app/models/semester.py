from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.core.db import Base


class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)


    classes = relationship("Class", back_populates="semester", cascade="all, delete-orphan")
    personal_events = relationship("PersonalEvent", back_populates="semester", cascade="all, delete-orphan")
