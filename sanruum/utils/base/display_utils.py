from __future__ import annotations

from sanruum.ai_core.protocols.base import UserProfileProtocol
from sanruum.ai_core.protocols.health import HealthRecordProtocol
from sanruum.utils.base.logger import logger
from sanruum.utils.base.time_utils import convert_utc_to_timezone


def display_health_record(
        record: HealthRecordProtocol,
        user_profile: UserProfileProtocol,
) -> str:
    """
    Converts a health record's timestamp from utc to the user's preferred
    timezone and returns a formatted display string.

    Args:
        record (HealthRecordProtocol): An object with a 'timestamp' attribute
            (stored in UTC) and other health metrics.
        user_profile (UserProfileProtocol): An object or dict containing a
         'timezone' attribute (e.g, "Europe/Tallinn").

    Returns:
        str: A formatted string with the localized timestamp and key health metrics.
    """
    try:
        # Check required attributes exist
        if not hasattr(record, 'timestamp') or not hasattr(record, 'blood_sugar'):
            raise ValueError('Record is missing required attributes.')
        if not hasattr(user_profile, 'timezone'):
            raise ValueError('User profile is missing required attribute.')

        local_timestamp = convert_utc_to_timezone(
            record.timestamp, user_profile.timezone,
        )
        display_str = (
            f"Recorded on: {local_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            f'| Blood Sugar: {record.blood_sugar} mmol/L'
        )
        # Add more fields as needed
        return display_str
    except Exception as e:
        logger.error(f'Error displaying record: {e}')
        return 'Error displaying health record.'
