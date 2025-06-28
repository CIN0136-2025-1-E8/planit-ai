from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class File(Base):
    __tablename__ = "files"

    uuid = Column(String, primary_key=True, index=True)
    original_name = Column(String, nullable=False)
    new_name = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    uploaded_at = Column(String, nullable=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), index=True, nullable=False)

    owner = relationship("User", back_populates="files")
