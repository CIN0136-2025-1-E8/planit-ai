import io
import mimetypes
import os
import shutil
import uuid
from datetime import datetime
from typing import Any, Optional

from fastapi import File, HTTPException

from core import settings


def validate_file(file: File):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Bad Request")
    if file.size > settings.FILE_UPLOAD_SIZE_LIMIT_BYTES:
        raise HTTPException(status_code=413, detail="Request Entity Too Large")
    if file.content_type not in settings.FILE_UPLOAD_SUPPORTED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")


def validate_filename(filename: str) -> None:
    if ".." in filename or filename.startswith(('/', '\\')):
        raise HTTPException(status_code=404, detail="File Not Found")
    if not os.path.isfile(settings.UPLOAD_DIR / filename):
        raise HTTPException(status_code=404, detail="File Not Found")


def validate_filenames(filenames: list[str]) -> None:
    for filename in filenames:
        validate_filename(filename)


def get_buffered_reader_from_filename(filename: str) -> io.BufferedReader:
    validate_filename(filename)
    return io.open(settings.UPLOAD_DIR / filename, "rb")


def save_file(file_path: str, data: Any) -> datetime:
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(data.file, buffer)
    return datetime.now()


def generate_unique_filepath(original_filename: Optional[str] = None, mime_type: Optional[str] = None) -> str:
    if original_filename:
        ext = os.path.splitext(original_filename)[1]
    elif mime_type:
        ext = mimetypes.guess_extension(mime_type) or '.bin'
    else:
        ext = '.bin'

    unique_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join(settings.UPLOAD_DIR, unique_filename)
