from datetime import date, datetime, timedelta, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException, status, Form, Query
from fastapi.security import HTTPAuthorizationCredentials
from firebase_admin import auth
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.security import token_scheme
from app.crud import get_user_crud, get_lecture_crud, get_evaluation_crud, get_event_crud, CRUDUser, CRUDLecture, \
    CRUDEvaluation, CRUDEvent
from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserData, ScheduleResponse

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post("/register", response_model=UserData)
def register_user(
        name: str = Form(),
        nickname: str | None = Form(None),
        user_crud: CRUDUser = Depends(get_user_crud),
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(token_scheme)
):
    try:
        decoded_token = auth.verify_id_token(token.credentials)
        uid = decoded_token['uid']
        email = decoded_token['email']
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token for registration"
        )

    if user_crud.get(db, obj_uuid=uid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User profile already exists."
        )

    user_in = UserCreate(name=name, nickname=nickname, email=email, uuid=uid)
    user = user_crud.create(db=db, obj_in=user_in)
    return user


@user_router.get("/", response_model=UserData)
def get_user(
        user_crud: CRUDUser = Depends(get_user_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user = user_crud.get(db, obj_uuid=user.uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@user_router.put("/", response_model=UserData)
def update_user(
        new_name: str | None = Form(None),
        new_nickname: str | None = Form(None),
        new_email: str | None = Form(None),
        user_crud: CRUDUser = Depends(get_user_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user_new_data: UserUpdate = UserUpdate(
        name=new_name,
        nickname=new_nickname,
        email=new_email,
    )
    db_user = user_crud.get(db, obj_uuid=user.uuid)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = user_crud.update(db=db, db_obj=db_user, obj_in=user_new_data)
    return updated_user


@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_crud: CRUDUser = Depends(get_user_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user = user_crud.remove(db, obj_uuid=user.uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return


@user_router.get("/schedule", response_model=ScheduleResponse)
def get_schedule(
        start_date: date = Query(
            default_factory=date.today,
            description="The start date for the period (format YYYY-MM-DD).",
        ),
        days: int = Query(
            default=7,
            description="The number of days in the period, including the start_date",
        ),
        timezone: str = Query(
            default="America/Recife",
            description="The client's IANA timezone name (e.g., 'America/Sao_Paulo', 'Europe/Paris').",
        ),
        lecture_crud: CRUDLecture = Depends(get_lecture_crud),
        evaluation_crud: CRUDEvaluation = Depends(get_evaluation_crud),
        event_crud: CRUDEvent = Depends(get_event_crud),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """
    Returns a user's schedule for a given period, interpreted according to the
    client's timezone. Lectures and evaluations are grouped by course.
    """
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        client_tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid timezone identifier: '{timezone}'"
        )

    start_of_period_local = datetime.combine(start_date, time.min, tzinfo=client_tz)
    end_date = start_date + timedelta(days=days)
    end_of_period_local = datetime.combine(end_date, time.min, tzinfo=client_tz)

    start_utc = start_of_period_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_of_period_local.astimezone(ZoneInfo("UTC"))

    lectures = lecture_crud.get_lectures_by_owner(
        db, owner_uuid=user.uuid, start_utc=start_utc, end_utc=end_utc, limit=1000
    )
    evaluations = evaluation_crud.get_evaluations_by_owner(
        db, owner_uuid=user.uuid, start_utc=start_utc, end_utc=end_utc, limit=1000
    )
    events = event_crud.get_events_by_owner(
        db, owner_uuid=user.uuid, start_utc=start_utc, end_utc=end_utc, limit=1000
    )

    for item in lectures + evaluations + events:
        item.start_datetime = item.start_datetime.astimezone(client_tz)
        item.end_datetime = item.end_datetime.astimezone(client_tz)

    schedule_by_day = {
        (start_date + timedelta(days=i)).isoformat(): []
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
                "start_datetime": lecture.start_datetime,
                "end_datetime": lecture.end_datetime,
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
                "start_datetime": evaluation.start_datetime,
                "end_datetime": evaluation.end_datetime,
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
                "start_datetime": event.start_datetime,
                "end_datetime": event.end_datetime,
            })

    for day_data in schedule_by_day.values():
        day_data.sort(key=lambda item: item['start_datetime'])

    return schedule_by_day
