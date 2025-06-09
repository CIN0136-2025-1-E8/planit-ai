from app.crud.base import CRUDBase
from app.models.semester import Semester
from app.schemas.semester import SemesterCreate, SemesterUpdate


class CRUDSemester(CRUDBase[Semester, SemesterCreate, SemesterUpdate]):
    pass


semester = CRUDSemester(Semester)
