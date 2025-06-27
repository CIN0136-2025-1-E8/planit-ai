from datetime import datetime

from pydantic import BaseModel


class FileRecord(BaseModel):
    original_filename: str
    content_type: str
    size: int
    uploaded_at: datetime
    url: str
