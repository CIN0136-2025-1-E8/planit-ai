from datetime import datetime
from zoneinfo import ZoneInfo


def to_utc_iso(dt_str: str, client_tz: ZoneInfo) -> str:
    """Converts a naive datetime string to an aware UTC ISO string."""
    try:
        dt_naive = datetime.fromisoformat(dt_str)
        dt_aware = dt_naive.replace(tzinfo=client_tz)
        dt_utc = dt_aware.astimezone(ZoneInfo("UTC"))
        return dt_utc.isoformat().replace("+00:00", "Z")
    except (ValueError, TypeError):
        return dt_str
