from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String, nullable=True)

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    class_ = relationship("Class", back_populates="schedules")
