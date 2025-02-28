from __future__ import annotations

from datetime import datetime
from datetime import timezone
from zoneinfo import ZoneInfo

from sanruum.utils.base.time_utils import convert_timezone_to_utc
from sanruum.utils.base.time_utils import convert_utc_to_timezone


def test_convert_utc_to_timezone() -> None:
    # Create a datetime in UTC (with tzinfo)
    dt_utc = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    # Convert to "Europe/Tallinn" (should be UTC+2 in January)
    dt_tallinn = convert_utc_to_timezone(dt_utc, 'Europe/Tallinn')

    # Expected datetime: adjust dt_utc to Europe/Tallinn
    # time zone using zoneinfo directly.
    expected_dt = dt_utc.astimezone(ZoneInfo('Europe/Tallinn'))
    assert dt_tallinn == expected_dt, f'Expected {expected_dt}, got {dt_tallinn}'


def test_convert_timezone_to_utc() -> None:
    # Create a datetime in "Europe/Tallinn" timezone
    dt_tallinn = datetime(
        2023, 1, 1, 14, 0, 0,
        tzinfo=ZoneInfo('Europe/Tallinn'),
    )
    # Convert to UTC using our function.
    dt_utc = convert_timezone_to_utc(dt_tallinn, 'Europe/Tallinn')

    # Expected datetime: dt_tallinn converted to UTC
    expected_dt = dt_tallinn.astimezone(ZoneInfo('UTC'))
    assert dt_utc == expected_dt, f'Expected {expected_dt}, got {dt_utc}'


def test_round_trip_conversion() -> None:
    # Start with a datetime in UTC.
    original_utc = datetime(
        2023, 1, 1, 12, 0, 0,
        tzinfo=timezone.utc,
    )
    # Convert to user's timezone.
    user_tz = 'Europe/Tallinn'
    local_time = convert_utc_to_timezone(original_utc, user_tz)
    # Now convert back to UTC.
    converted_back = convert_timezone_to_utc(local_time, user_tz)
    # They should match (within possible microsecond differences)
    assert abs(
        (converted_back - original_utc).total_seconds(),
    ) < 1, 'Round-trip conversion failed'
