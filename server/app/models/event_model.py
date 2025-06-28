import uuid

from sqlalchemy import Column, String, Text, ForeignKey, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class Event(Base):
    __tablename__ = 'events'

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_datetime = Column(String, nullable=False)
    end_datetime = Column(String, nullable=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), nullable=True)

    owner = relationship("User", back_populates="events")
