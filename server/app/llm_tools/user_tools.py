import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.orm import Session

from app.crud import evaluation_crud, lecture_crud, event_crud
from app.dependencies import get_db
from app.models import Lecture as LectureModel, Evaluation as EvaluationModel, Event as EventModel


async def get_user_schedule(
        user_uuid: str,
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

        start_date = datetime.date.fromisoformat(start_date_str)

        start_of_period_local = datetime.datetime.combine(start_date, datetime.time.min, tzinfo=client_tz)
        end_date = start_date + datetime.timedelta(days=days)
        end_of_period_local = datetime.datetime.combine(end_date, datetime.time.min, tzinfo=client_tz)

        start_utc = start_of_period_local.astimezone(ZoneInfo("UTC"))
        end_utc = end_of_period_local.astimezone(ZoneInfo("UTC"))

        lectures: list[LectureModel] = lecture_crud.get_lectures_by_owner(
            db, owner_uuid=user_uuid, start_utc=start_utc, end_utc=end_utc, limit=1000,
        )
        evaluations: list[EvaluationModel] = evaluation_crud.get_evaluations_by_owner(
            db, owner_uuid=user_uuid, start_utc=start_utc, end_utc=end_utc, limit=1000,
        )
        events: list[EventModel] = event_crud.get_events_by_owner(
            db, owner_uuid=user_uuid, start_utc=start_utc, end_utc=end_utc, limit=1000,
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


user_tools = [get_user_schedule]
