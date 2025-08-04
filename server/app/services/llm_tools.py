import datetime

from sqlalchemy.orm import Session

from app.core import settings
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


async def list_courses() -> dict:
    """
    Para ler uma lista resumida de todos os cursos disponíveis para o usuário atual.

    Returns:
        Um dicionário com uma chave 'courses' contendo uma lista resumida de todos os cursos disponíveis para o
        usuário atual, que sempre inclui o uuid e título de cada curso, e pode incluir o semestre daquele curso, se
        essa informação estiver disponível.
        Caso ocorra algum erro na execução da função, o dicionário conterá apenas as informações do erro.
    """
    try:
        db: Session = next(get_db())
        course_crud = get_course_crud()
        current_user: User = await get_current_user(db=db)
        courses = course_crud.get_all_by_owner_uuid(db=db, owner_uuid=current_user.uuid)
        return {"courses": [CourseSummary.model_validate(course).model_dump(mode='json') for course in courses]}
    except Exception as e:
        return {"error": f"An error occurred while listing course summaries.: {e}."}


async def list_full_courses() -> dict:
    """
    Lista todas as informações de cada curso do usuário atual, incluindo aulas e avaliações.

    Returns:
        Um dicionário com uma chave 'courses' contendo uma lista de cursos completos.
        Caso ocorra algum erro na execução da função, o dicionário conterá apenas as informações do erro.
    """
    try:
        db: Session = next(get_db())
        course_crud = get_course_crud()
        current_user: User = await get_current_user(db=db)
        courses = course_crud.get_all_by_owner_uuid(db=db, owner_uuid=current_user.uuid)
        return {"courses": [Course.model_validate(course).model_dump(mode='json') for course in courses]}
    except Exception as e:
        return {"error": f"An error occurred while listing full courses: {e}."}


tools = [
    get_current_utc_time,
    list_courses,
    list_full_courses,
]
