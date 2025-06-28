import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    start_datetime = Column(String, nullable=False)
    end_datetime = Column(String, nullable=False)
    present = Column(Boolean, nullable=False, default=False)

    course_uuid = Column(String, ForeignKey("courses.uuid"), nullable=False)

    course = relationship("Course", back_populates="evaluations")
