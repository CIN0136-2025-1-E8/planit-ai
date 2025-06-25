from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Operation(Base):
    __tablename__ = "operations"

    uuid = Column(String, primary_key=True)
    order = Column(Integer, nullable=False)
    batch_uuid = Column(String, nullable=False)
    operation_data = Column(Text, nullable=False)
    inverse_operation_data = Column(Text, nullable=False)
    timestamp = Column(String, default=str(datetime.now), nullable=False)
    is_undone = Column(Boolean, default=False, nullable=False)

    owner_id = Column(String, ForeignKey("user.uuid"), nullable=False)

    owner = relationship("User", back_populates="operation_log")
