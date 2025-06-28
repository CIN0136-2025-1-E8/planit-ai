import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Uuid, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db import Base


class File(Base):
    __tablename__ = "files"

    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=uuid.uuid4)
    original_name = Column(String, nullable=False)
    new_name = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    uploaded_at = Column(String, nullable=False)

    owner_uuid = Column(String, ForeignKey("users.uuid"), nullable=False)

    owner = relationship("User", back_populates="files")
