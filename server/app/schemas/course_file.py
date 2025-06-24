from enum import Enum

from pydantic import BaseModel, ConfigDict

from schemas.files import FileRecord


class CourseFilePurposeEnum(Enum):
    CRONOGRAMA = "CRONOGRAMA"  # Apenas um exemplo. Deve ser traduzido ou trocado.
    # Adicionar os outros.


class CourseFileBase(BaseModel):
    purpose: CourseFilePurposeEnum
    metadata: FileRecord


class CourseFileCreate(CourseFileBase):
    course_uuid: str


class CourseFileUpdate(BaseModel):
    purpose: CourseFilePurposeEnum | None = None
    metadata: FileRecord | None = None


class CourseFile(CourseFileBase):
    uuid: str
    model_config = ConfigDict(from_attributes=True)
