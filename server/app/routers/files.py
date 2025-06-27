import os
from typing import Dict

from fastapi import APIRouter, UploadFile
from starlette import status

from crud import files_crud
from schemas import FileRecord
from utils import file_handling

files_router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={400: {"description": "Bad Request"},
               404: {"description": "File not found"},
               413: {"description": "Request Entity Too Large"},
               415: {"description": "Unsupported Media Type"}}
)


@files_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile) -> FileRecord:
    file_handling.validate_file(file)
    new_file_path = file_handling.generate_unique_filepath(original_filename=file.filename)
    uuid_filename = os.path.basename(new_file_path)
    uploaded_at = file_handling.save_file(new_file_path, file)
    return files_crud.create_file_record(uuid_filename=uuid_filename,
                                         original_filename=file.filename,
                                         content_type=file.content_type,
                                         size=file.size,
                                         uploaded_at=uploaded_at,
                                         url=f"/files/{uuid_filename}")


@files_router.get("/")
async def get_file_list() -> Dict[str, FileRecord]:
    return files_crud.get_all_file_records()
