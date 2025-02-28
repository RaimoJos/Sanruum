from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo


def convert_utc_to_timezone(dt: datetime, tz_str: str) -> datetime:
    """
    Converts a UTC datetime to the specified timezone.

    Args:
        dt (datetime): The datetime in UTC.
        tz_str (str): The targret timezone string (e.g., "Europe/Tallinn").

    Returns:
        datetime: The datetime adjusted to the target timezone.
    """
    return dt.astimezone(ZoneInfo(tz_str))


def convert_timezone_to_utc(dt: datetime, tz_str: str) -> datetime:
    """
    Converts a datetime in a given timezone to UTC.

    Args:
        dt (datetime): The datetime in the local timezone.
        tz_str (str): The timezone string of dt.

    Returns:
        datetime: The datetime converted to UTC.
    """
    local_dt = dt.replace(tzinfo=ZoneInfo(tz_str))
    return local_dt.astimezone(ZoneInfo('UTC'))
