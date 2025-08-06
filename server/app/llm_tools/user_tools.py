import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import user_crud, evaluation_crud, lecture_crud, event_crud
from app.dependencies import get_db
from app.models import User as UserModel, Lecture as LectureModel, Evaluation as EvaluationModel, Event as EventModel
from app.schemas import UserUpdate


async def get_user_profile() -> dict:
    """
    Retrieves the profile information for the currently authenticated user.

    :return: A dictionary containing a success flag and the user's profile data
             (name, nickname, and email), or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        user_profile: dict = {
            "name": user.name,
            "nickname": user.nickname,
            "email": user.email,
        }
        return {"success": True, "user_profile": user_profile}
    except Exception as e:
        return {"error": f"Error while retrieving the user profile: {e}"}


async def update_user_profile(
        new_name: str | None = None,
        new_nickname: str | None = None,
) -> dict:
    """
    Updates the profile information for the currently authenticated user.

    This tool can be used to change the user's name and/or nickname.
    For security reasons, changing the email or password must be done by the user
    directly through the application's interface.

    :param new_name: The user's new full name.
    :param new_nickname: The user's new nickname.
    :return: A dictionary containing a success flag and the updated user profile data,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_user = user_crud.get(db, obj_uuid=user.uuid)
        if not db_user:
            return {"error": "User not found."}

        user_update = UserUpdate(name=new_name, nickname=new_nickname)

        updated_user_db = user_crud.update(db=db, db_obj=db_user, obj_in=user_update)
        updated_user = {
            "name": updated_user_db.name,
            "nickname": updated_user_db.nickname,
            "email": updated_user_db.email,
        }

        return {"success": True, "user_profile": updated_user}
    except Exception as e:
        return {"error": f"Error while updating the user profile: {e}"}


async def get_user_schedule(
        start_date_str: str | None = None,
        days: int | None = None,
        timezone: str | None = None,
) -> dict:
    """
    Retrieves a user's schedule for a specified period, including lectures, evaluations, and events.

    The schedule is returned grouped by day, and all times are adjusted to the requested timezone.

    :param start_date_str: The start date for the schedule period in 'YYYY-MM-DD' format.
                           If not provided, the current date will be used.
    :param days: The total number of days to include in the schedule, starting from the start_date.
                 Defaults to 7.
    :param timezone: The user's IANA timezone name (e.g., 'America/Sao_Paulo', 'Europe/Paris')
                     to be used for interpreting the schedule times. Defaults to 'America/Recife'.
    :return: A dictionary containing a success flag and the schedule data,
             or an error key with a descriptive message.
    """
    try:
        if not start_date_str:
            start_date_str = str(datetime.date.today())
        if not days:
            days = 7
        if not timezone:
            timezone = 'America/Recife'
        try:
            client_tz = ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            return {"error": f"Invalid timezone identifier: '{timezone}'"}

        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        start_date = datetime.date.fromisoformat(start_date_str)

        start_of_period_local = datetime.datetime.combine(start_date, datetime.time.min, tzinfo=client_tz)
        end_date = start_date + datetime.timedelta(days=days)
        end_of_period_local = datetime.datetime.combine(end_date, datetime.time.min, tzinfo=client_tz)

        start_utc = start_of_period_local.astimezone(ZoneInfo("UTC"))
        end_utc = end_of_period_local.astimezone(ZoneInfo("UTC"))

        lectures: list[LectureModel] = lecture_crud.get_lectures_by_owner(
            db, owner_uuid=user.uuid, start_utc=start_utc, end_utc=end_utc, limit=1000,
        )
        evaluations: list[EvaluationModel] = evaluation_crud.get_evaluations_by_owner(
            db, owner_uuid=user.uuid, start_utc=start_utc, end_utc=end_utc, limit=1000,
        )
        events: list[EventModel] = event_crud.get_events_by_owner(
            db, owner_uuid=user.uuid, start_utc=start_utc, end_utc=end_utc, limit=1000,
        )

        all_items = lectures + evaluations + events
        for item in all_items:
            item.start_datetime = item.start_datetime.astimezone(client_tz)
            item.end_datetime = item.end_datetime.astimezone(client_tz)

        schedule_by_day = {
            (start_date + datetime.timedelta(days=i)).isoformat(): []
            for i in range(days)
        }

        for lecture in lectures:
            day_str = lecture.start_datetime.date().isoformat()
            if day_str in schedule_by_day:
                schedule_by_day[day_str].append({
                    "item_type": "lecture",
                    "course_uuid": lecture.course.uuid,
                    "course_title": lecture.course.title,
                    "uuid": lecture.uuid,
                    "title": lecture.title,
                    "start_datetime": lecture.start_datetime.isoformat(),
                    "end_datetime": lecture.end_datetime.isoformat(),
                    "summary": lecture.summary,
                })

        for evaluation in evaluations:
            day_str = evaluation.start_datetime.date().isoformat()
            if day_str in schedule_by_day:
                schedule_by_day[day_str].append({
                    "item_type": "evaluation",
                    "course_uuid": evaluation.course.uuid,
                    "course_title": evaluation.course.title,
                    "uuid": evaluation.uuid,
                    "title": evaluation.title,
                    "start_datetime": evaluation.start_datetime.isoformat(),
                    "end_datetime": evaluation.end_datetime.isoformat(),
                    "type": evaluation.type,
                })

        for event in events:
            day_str = event.start_datetime.date().isoformat()
            if day_str in schedule_by_day:
                schedule_by_day[day_str].append({
                    "item_type": "event",
                    "uuid": event.uuid,
                    "title": event.title,
                    "description": event.description,
                    "start_datetime": event.start_datetime.isoformat(),
                    "end_datetime": event.end_datetime.isoformat(),
                })

        for day_data in schedule_by_day.values():
            day_data.sort(key=lambda item: item['start_datetime'])

        return {"success": True, "schedule": schedule_by_day}
    except Exception as e:
        return {"error": f"Error while retrieving the user schedule: {e}"}


user_tools = [get_user_profile, update_user_profile, get_user_schedule]
