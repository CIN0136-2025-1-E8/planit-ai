import datetime

from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import get_course_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import Course, CourseSummary


def get_current_utc_time() -> dict:
    """Gets the current time in UTC.

    Returns:
        A dictionary containing the current UTC time in ISO 8601 format.
        Example: {"utc_time": "2023-10-27T10:00:00.123456"}
    """
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    iso_format_time = utc_now.isoformat()
    return {"utc_time": iso_format_time}


async def list_course_summaries() -> dict:
    """
    Lista os resumos de todos os cursos disponíveis para o usuário atual.

    Returns:
        Um dicionário com uma chave 'courses' contendo uma lista de resumos de curso,
        ou um dicionário de erro.
    """
    try:
        db: Session = next(get_db())
        course_crud = get_course_crud()
        current_user: User = await get_current_user(db=db)
        courses = course_crud.get_all_by_owner_uuid(db=db, owner_uuid=current_user.uuid)
        return {"courses": [CourseSummary.model_validate(course).model_dump() for course in courses]}
    except Exception as e:
        return {"error": f"An error occurred while listing course summaries.: {e}."}


async def list_full_courses() -> dict:
    """
    Lista todas as informações de cada curso do usuário atual, incluindo aulas e avaliações.

    Returns:
        Um dicionário com uma chave 'courses' contendo uma lista de cursos completos,
        ou um dicionário de erro.
    """
    try:
        db: Session = next(get_db())
        course_crud = get_course_crud()
        current_user: User = await get_current_user(db=db)
        courses = course_crud.get_all_by_owner_uuid(db=db, owner_uuid=current_user.uuid)
        return {"courses": [Course.model_validate(course).model_dump() for course in courses]}
    except Exception as e:
        return {"error": f"An error occurred while listing full courses: {e}."}


tools = [get_current_utc_time, list_course_summaries, list_full_courses]
