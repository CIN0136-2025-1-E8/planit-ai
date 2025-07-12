from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Event(Base):
    __tablename__ = 'events'

    uuid = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_datetime = Column(String, nullable=False)
    end_datetime = Column(String, nullable=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), index=True, nullable=False)

    owner = relationship("User", back_populates="events")
