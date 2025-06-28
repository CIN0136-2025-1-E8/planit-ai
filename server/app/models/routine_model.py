import uuid

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class Routine(Base):
    __tablename__ = 'routines'

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    flexible = Column(Boolean, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    days_of_the_week = Column(Integer, nullable=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), nullable=True)

    owner = relationship("User", back_populates="routines")

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 4
    WEDNESDAY = 8
    THURSDAY = 16
    FRIDAY = 32
    SATURDAY = 64
