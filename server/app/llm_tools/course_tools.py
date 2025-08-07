from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import get_course_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import Course, CourseSummary, CourseUpdate, CourseCreate, CourseDeleteResponse


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


async def list_courses_and_details() -> dict:
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


async def create_course(title: str, semester: str | None = None) -> dict:
    """
    Cria um curso vazio (sem aulas ou avaliações).
    """
    try:
        db: Session = next(get_db())
        current_user: User = await get_current_user(db=db)
        course_crud = get_course_crud()

        course_in = CourseCreate(title=title, semester=semester, owner_uuid=current_user.uuid)
        db_course = course_crud.create(db=db, obj_in=course_in)
        created_course = Course.model_validate(db_course)

        return {"success": True, "course": created_course.model_dump(mode='json')}
    except Exception as e:
        return {"error": f"Ocorreu um erro ao criar o curso: {e}"}


async def update_course(course_uuid: str, new_title: str | None = None, new_semester: str | None = None) -> dict:
    """
    Atualiza os detalhes de um curso específico, como seu título ou semestre.
    """
    try:
        db: Session = next(get_db())
        course_crud = get_course_crud()
        user: User = await get_current_user(db=db)

        db_course = course_crud.get(db=db, obj_uuid=course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Curso não encontrado."}

        update_data = CourseUpdate(title=new_title, semester=new_semester).model_dump(exclude_unset=True)
        if not update_data:
            return {"error": "Nenhum dado fornecido para atualização."}

        db_course = course_crud.update(db=db, db_obj=db_course, obj_in=update_data)
        updated_course = Course.model_validate(db_course)
        return {"success": True, "course": updated_course.model_dump(mode='json')}
    except Exception as e:
        return {"error": f"Ocorreu um erro ao atualizar o curso: {e}"}


async def delete_course(course_uuid: str) -> dict:
    """
    Apaga um curso específico e todos os seus dados associados (aulas, avaliações).
    """
    try:
        db: Session = next(get_db())
        course_crud = get_course_crud()
        user: User = await get_current_user(db=db)

        db_course = course_crud.get(db=db, obj_uuid=course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Curso não encontrado."}

        db_course = course_crud.remove(db=db, obj_uuid=course_uuid)
        removed_course = CourseDeleteResponse.model_validate(db_course)
        removed_course.deleted_lectures = len(db_course.lectures)
        removed_course.deleted_evaluations = len(db_course.evaluations)
        return {"success": True,
                "message": f"Curso '{removed_course.title}' e suas {removed_course.deleted_lectures} aulas e {removed_course.deleted_evaluations} avaliações foram apagados."}
    except Exception as e:
        return {"error": f"Ocorreu um erro ao apagar o curso: {e}"}


course_tools = [
    list_courses,
    list_courses_and_details,
    create_course,
    update_course,
    delete_course,
]
