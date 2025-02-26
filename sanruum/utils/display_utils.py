from __future__ import annotations

from typing import Any

from sanruum.utils.time_utils import convert_utc_to_timezone


def display_health_record(record: Any, user_profile: Any) -> str:
    """
    Converts a health record's timestamp from utc to the user's preferred
    timezone and returns a formatted display string.

    Args:
        record: An object with a 'timestamp' attribute (stored in UTC) and
            other health metrics.
        user_profile: An object or dict containing a 'timezone' attribute
            (e.g, "Europe/Tallinn").

    Returns:
        str: A formatted string with the localized timestamp and key health metrics.
    """
    local_timestamp = convert_utc_to_timezone(
        record.timestampm, user_profile.timezone,
    )
    display_str = (
        f"Recorded on: {local_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        f'| Blood Sugar: {record.blood_sugar} mmol/L'
    )
    # Add more fields as needed
    return display_str
