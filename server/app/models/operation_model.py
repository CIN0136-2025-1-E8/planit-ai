import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class Operation(Base):
    __tablename__ = "operations"

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    order = Column(Integer, nullable=False)
    batch_uuid = Column(String, nullable=False)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    target_uuid = Column(String, nullable=True)
    parent_uuid = Column(String, nullable=True)
    is_undone = Column(Boolean, default=False, nullable=False)
    operation_data = Column(Text, nullable=False)
    inverse_operation_data = Column(Text, nullable=False)
    timestamp = Column(String, default=str(datetime.now), nullable=False)

    owner_id = Column(String, ForeignKey("users.uuid"), nullable=False)

    owner = relationship("User", back_populates="operation_log")
