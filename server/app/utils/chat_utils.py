from datetime import datetime

from app.core import settings


def system_message_current_datetime() -> str:
    return "".join([settings.SYSTEM_MESSAGE_MARKER_START,
                    "The current date and time is ",
                    str(datetime.now()),
                    settings.SYSTEM_MESSAGE_MARKER_END])
