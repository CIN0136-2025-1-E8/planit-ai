import os
import pickle
from datetime import datetime
from typing import Dict

from core import settings
from schemas import FileRecord


class CRUDFiles:
    file_list: Dict[str, FileRecord] = {}

    def read_file_list_from_file(self) -> None:
        if os.path.exists(settings.DEBUG_FILE_LIST_FILE_PATH):
            with open(settings.DEBUG_FILE_LIST_FILE_PATH, 'rb') as file:
                self.file_list = pickle.load(file)
        return

    def write_file_list_to_file(self) -> None:
        with open(settings.DEBUG_FILE_LIST_FILE_PATH, "wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.file_list, f)
        return

    def create_file_record(self, uuid_filename: str,
                           original_filename: str,
                           content_type: str,
                           size: int,
                           uploaded_at: datetime,
                           url: str) -> FileRecord:
        record = FileRecord(
            original_filename=original_filename,
            content_type=content_type,
            size=size,
            uploaded_at=uploaded_at,
            url=url)
        self.file_list[uuid_filename] = record
        self.write_file_list_to_file()
        return record

    def get_all_file_records(self):
        return self.file_list

    def get_file_by_uuid_filename(self, file_uuid_filename: str):
        return self.file_list.get(file_uuid_filename)

    def delete_file_by_uuid_filename(self, file_uuid_filename: str):
        self.write_file_list_to_file()
        return self.file_list.pop(file_uuid_filename)


files_crud = CRUDFiles()
