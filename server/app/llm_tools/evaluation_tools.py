from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import evaluation_crud, course_crud
from app.dependencies import get_db
from app.models import User as UserModel, Evaluation as EvaluationModel, Course as CourseModel
from app.schemas import EvaluationCreate, EvaluationUpdate, EvaluationTypes, Evaluation


async def create_evaluation(
        course_uuid: str,
        title: str,
        evaluation_type: str,
        start_datetime: str,
        end_datetime: str,
) -> dict:
    """
    Creates a new evaluation for a specific course.

    This function validates the user's authorization and the provided evaluation type,
    then creates an evaluation record in the database associated with the given course.

    :param course_uuid: The UUID of the course to which this evaluation belongs.
    :param title: The title of the evaluation.
    :param evaluation_type: The type of evaluation. Must be one of the following: 'exam', 'quiz', 'assignment', 'presentation' or 'lab'.
    :param start_datetime: The UTC start date and time for the evaluation in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param end_datetime: The UTC end date and time for the evaluation in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :return: A dictionary containing either a success flag and the created evaluation data,
             or an error key with a descriptive message.
    """
    try:
        valid_types = [e.value for e in EvaluationTypes]
        if evaluation_type not in valid_types:
            return {"error": f"Invalid evaluation type. Supported evaluation types: {valid_types}"}

        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_course: CourseModel = course_crud.get(db=db, obj_uuid=course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Course not found."}

        evaluation_in: EvaluationCreate = EvaluationCreate(
            course_uuid=course_uuid,
            title=title,
            type=EvaluationTypes(evaluation_type),
            start_datetime=datetime.fromisoformat(start_datetime),
            end_datetime=datetime.fromisoformat(end_datetime),
        )
        db_evaluation: EvaluationModel = evaluation_crud.create(db=db, obj_in=evaluation_in)
        created_evaluation: Evaluation = Evaluation.model_validate(db_evaluation)
        return {"success": True, "evaluation": created_evaluation.model_dump(mode="json")}
    except Exception as e:
        return {"error": f"Error while creating the evaluation: {e}"}


async def update_evaluation(
        evaluation_uuid: str,
        new_title: str | None = None,
        new_evaluation_type: str | None = None,
        new_start_datetime: str | None = None,
        new_end_datetime: str | None = None,
) -> dict:
    """
    Updates the details of a specific evaluation.

    This function allows for partial updates. Only the provided fields will be changed.
    It ensures the user is authorized to make changes to the evaluation.

    :param evaluation_uuid: The UUID of the evaluation to be updated.
    :param new_title: The new title for the evaluation, if it needs to be changed.
    :param new_evaluation_type: The new type for the evaluation. Must be one of the following: 'exam', 'quiz', 'assignment', 'presentation' or 'lab'.
    :param new_start_datetime: The new UTC start date and time in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param new_end_datetime: The new UTC end date and time in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :return: A dictionary containing a success flag and the updated evaluation data,
             or an error key with a descriptive message.
    """
    try:
        valid_types = [e.value for e in EvaluationTypes]
        if new_evaluation_type and new_evaluation_type not in valid_types:
            return {"error": f"Invalid evaluation type. Supported evaluation types: {valid_types}"}

        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_evaluation: EvaluationModel = evaluation_crud.get(db=db, obj_uuid=evaluation_uuid)
        if not db_evaluation:
            return {"error": "Evaluation not found."}

        db_course: CourseModel = course_crud.get(db=db, obj_uuid=db_evaluation.course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Evaluation not found."}

        evaluation_update: EvaluationUpdate = EvaluationUpdate(
            title=new_title,
            type=new_evaluation_type,
            start_datetime=new_start_datetime,
            end_datetime=new_end_datetime,
        )
        updated_db_evaluation = evaluation_crud.update(db=db, db_obj=db_evaluation, obj_in=evaluation_update)
        updated_evaluation: Evaluation = Evaluation.model_validate(updated_db_evaluation)
        return {"success": True, "evaluation": updated_evaluation.model_dump(mode='json')}
    except Exception as e:
        return {"error": f"Error while updating the evaluation: {e}"}


async def delete_evaluation(evaluation_uuid: str) -> dict:
    """
    Deletes a specific evaluation from the database.

    This function verifies that the user is authorized to delete the evaluation
    before permanently removing it.

    :param evaluation_uuid: The UUID of the evaluation to be deleted.
    :return: A dictionary containing a success flag and a confirmation message,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_evaluation: EvaluationModel = evaluation_crud.get(db=db, obj_uuid=evaluation_uuid)
        if not db_evaluation:
            return {"error": "Evaluation not found."}

        db_course: CourseModel = course_crud.get(db=db, obj_uuid=db_evaluation.course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Evaluation not found."}

        removed_db_evaluation: EvaluationModel = evaluation_crud.remove(db=db, obj_uuid=evaluation_uuid)
        if not removed_db_evaluation:
            return {"error": "Evaluation not found."}

        return {"success": True, "message": f"Evaluation '{removed_db_evaluation.title}' deleted."}
    except Exception as e:
        return {"error": f"Error while deleting evaluation: {e}"}


evaluation_tools = [create_evaluation, update_evaluation, delete_evaluation]
