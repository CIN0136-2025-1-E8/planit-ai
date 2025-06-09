from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class ScheduleOverride(Base):
    __tablename__ = "schedule_overrides"

    id = Column(Integer, primary_key=True, index=True)
    override_date = Column(Date, nullable=False, index=True)
    is_cancelled = Column(Boolean, default=False, nullable=False)
    notes = Column(String, nullable=True)
    new_start_time = Column(Time, nullable=True)
    new_end_time = Column(Time, nullable=True)
    new_location = Column(String, nullable=True)

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    class_ = relationship("Class", back_populates="overrides")
