from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import event_crud
from app.dependencies import get_db
from app.models import User as UserModel, Event as EventModel
from app.schemas import EventCreate, EventUpdate, Event, EventCreateInDB


async def create_event(
        title: str,
        start_datetime: str,
        end_datetime: str,
        description: str | None = None,
) -> dict:
    """
    Creates a new event for the current user. Events can be personal events, holidays, and appointments,
    but also instances of user routines, such as specific study sessions with a set of chosen subjects.

    :param title: The title of the event.
    :param start_datetime: The UTC start date and time for the event in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param end_datetime: The UTC end date and time for the event in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param description: A description of the event's content.
    :return: A dictionary containing either a success flag and the created event data,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        event_in = EventCreate(
            title=title,
            description=description,
            start_datetime=datetime.fromisoformat(start_datetime),
            end_datetime=datetime.fromisoformat(end_datetime),
        )

        event_in_db = EventCreateInDB(**event_in.model_dump(), owner_uuid=user.uuid)

        db_event: EventModel = event_crud.create(db=db, obj_in=event_in_db)
        created_event: Event = Event.model_validate(db_event)
        return {"success": True, "event": created_event.model_dump(mode="json")}
    except Exception as e:
        return {"error": f"Error while creating the event: {e}"}


async def update_event(
        event_uuid: str,
        new_title: str | None = None,
        new_description: str | None = None,
        new_start_datetime: str | None = None,
        new_end_datetime: str | None = None,
) -> dict:
    """
    Updates the details of a specific event (e.g., personal event, holiday, study session).

    This function allows for partial updates. Only the provided fields will be changed.
    It ensures the user is authorized to make changes to the event.

    :param event_uuid: The UUID of the event to be updated.
    :param new_title: The new title for the event, if it needs to be changed.
    :param new_description: The new description for the event.
    :param new_start_datetime: The new UTC start date and time in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :param new_end_datetime: The new UTC end date and time in ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ').
    :return: A dictionary containing a success flag and the updated event data,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_event: EventModel = event_crud.get(db=db, obj_uuid=event_uuid)
        if not db_event or db_event.owner_uuid != user.uuid:
            return {"error": "Event not found."}

        update_data = {
            "title": new_title,
            "description": new_description,
            "start_datetime": datetime.fromisoformat(new_start_datetime) if new_start_datetime else None,
            "end_datetime": datetime.fromisoformat(new_end_datetime) if new_end_datetime else None,
        }

        event_update = EventUpdate(**update_data)

        updated_db_event = event_crud.update(db=db, db_obj=db_event, obj_in=event_update)
        updated_event: Event = Event.model_validate(updated_db_event)
        return {"success": True, "event": updated_event.model_dump(mode='json')}
    except Exception as e:
        return {"error": f"Error while updating the event: {e}"}


async def delete_event(event_uuid: str) -> dict:
    """
    Deletes a specific event (e.g., personal event, holiday, study session) from the database.

    This function verifies that the user is authorized to delete the event
    before permanently removing it.

    :param event_uuid: The UUID of the event to be deleted.
    :return: A dictionary containing a success flag and a confirmation message,
             or an error key with a descriptive message.
    """
    try:
        db: Session = next(get_db())

        user: UserModel = await get_current_user(db=db)
        if not user:
            return {"error": "User not authorized."}

        db_event: EventModel = event_crud.get(db=db, obj_uuid=event_uuid)
        if not db_event or db_event.owner_uuid != user.uuid:
            return {"error": "Event not found."}

        removed_db_event: EventModel = event_crud.remove(db=db, obj_uuid=event_uuid)
        if not removed_db_event:
            return {"error": "Event not found."}

        return {"success": True, "message": f"Event '{removed_db_event.title}' deleted."}
    except Exception as e:
        return {"error": f"Error while deleting event: {e}"}


event_tools = [create_event, update_event, delete_event]
