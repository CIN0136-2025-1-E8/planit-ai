from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class PersonalEvent(Base):
    __tablename__ = "personal_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    event_type = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)


    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=True)
    semester = relationship("Semester", back_populates="personal_events")
