from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import lecture_crud, course_crud
from app.dependencies import get_db
from app.models import User as UserModel, Lecture as LectureModel, Course as CourseModel
from app.schemas import LectureCreate, LectureUpdate, Lecture


async def create_lecture(
        course_uuid: str,
        title: str,
        start_datetime: str,
        end_datetime: str,
        summary: str | None = None,
) -> dict:
    """
    Creates a new lecture for a specific course.

    This function validates the user's authorization,
    then creates a lecture record in the database associated with the given course.

    :param course_uuid: The UUID of the course to which this lecture belongs.
    :param title: The title of the lecture.
    :param start_datetime: The UTC start date and time for the lecture in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param end_datetime: The UTC end date and time for the lecture in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param summary: A brief summary of the lecture's content.
    :return: A dictionary containing either a success flag and the created lecture data,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_course: CourseModel = course_crud.get(db=db, obj_uuid=course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Course not found."}

        lecture_in: LectureCreate = LectureCreate(
            course_uuid=course_uuid,
            title=title,
            start_datetime=datetime.fromisoformat(start_datetime),
            end_datetime=datetime.fromisoformat(end_datetime),
            summary=summary,
        )
        db_lecture: LectureModel = lecture_crud.create(db=db, obj_in=lecture_in)
        created_lecture: Lecture = Lecture.model_validate(db_lecture)
        return {"success": True, "lecture": created_lecture.model_dump(mode="json")}
    except Exception as e:
        return {"error": f"Error while creating the lecture: {e}"}


async def update_lecture(
        lecture_uuid: str,
        new_title: str | None = None,
        new_start_datetime: str | None = None,
        new_end_datetime: str | None = None,
        new_summary: str | None = None,
        new_present: bool | None = None,
) -> dict:
    """
    Updates the details of a specific lecture.

    This function allows for partial updates. Only the provided fields will be changed.
    It ensures the user is authorized to make changes to the lecture.

    :param lecture_uuid: The UUID of the lecture to be updated.
    :param new_title: The new title for the lecture, if it needs to be changed.
    :param new_start_datetime: The new UTC start date and time in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param new_end_datetime: The new UTC end date and time in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param new_summary: The new summary for the lecture.
    :param new_present: The new user presence status for the lecture.
    :return: A dictionary containing a success flag and the updated lecture data,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_lecture: LectureModel = lecture_crud.get(db=db, obj_uuid=lecture_uuid)
        if not db_lecture:
            return {"error": "Lecture not found."}

        db_course: CourseModel = course_crud.get(db=db, obj_uuid=db_lecture.course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Lecture not found."}

        lecture_update: LectureUpdate = LectureUpdate(
            title= new_title,
            summary= new_summary,
            present= new_present,
            start_datetime= datetime.fromisoformat(new_start_datetime) if new_start_datetime else None,
            end_datetime= datetime.fromisoformat(new_end_datetime) if new_end_datetime else None,
        )
        updated_db_lecture = lecture_crud.update(db=db, db_obj=db_lecture, obj_in=lecture_update)
        updated_lecture: Lecture = Lecture.model_validate(updated_db_lecture)
        return {"success": True, "lecture": updated_lecture.model_dump(mode='json')}
    except Exception as e:
        return {"error": f"Error while updating the lecture: {e}"}


async def delete_lecture(lecture_uuid: str) -> dict:
    """
    Deletes a specific lecture from the database.

    This function verifies that the user is authorized to delete the lecture
    before permanently removing it.

    :param lecture_uuid: The UUID of the lecture to be deleted.
    :return: A dictionary containing a success flag and a confirmation message,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_lecture: LectureModel = lecture_crud.get(db=db, obj_uuid=lecture_uuid)
        if not db_lecture:
            return {"error": "Lecture not found."}

        db_course: CourseModel = course_crud.get(db=db, obj_uuid=db_lecture.course_uuid)
        if not db_course or db_course.owner_uuid != user.uuid:
            return {"error": "Lecture not found."}

        removed_db_lecture: LectureModel = lecture_crud.remove(db=db, obj_uuid=lecture_uuid)
        if not removed_db_lecture:
            return {"error": "Lecture not found."}

        return {"success": True, "message": f"Lecture '{removed_db_lecture.title}' deleted."}
    except Exception as e:
        return {"error": f"Error while deleting lecture: {e}"}


lecture_tools = [create_lecture, update_lecture, delete_lecture]
