from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from core.db import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    uuid = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    start_datetime = Column(String, nullable=False)
    end_datetime = Column(String, nullable=False)
    present = Column(Boolean, nullable=False, default=False)

    course_uuid = Column(String, ForeignKey("courses.uuid"), index=True, nullable=False)

    course = relationship("Course", back_populates="evaluations")
