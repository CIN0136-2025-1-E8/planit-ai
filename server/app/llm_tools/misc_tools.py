import datetime


def get_current_utc_time() -> dict:
    """Gets the current time in UTC.

    Returns:
        A dictionary containing the current UTC time in ISO 8601 format.
        Example: {"utc_time": "2023-10-27T10:00:00.123456"}
    """
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    iso_format_time = utc_now.isoformat()
    return {"utc_time": iso_format_time}


misc_tools = [
    get_current_utc_time,
]
