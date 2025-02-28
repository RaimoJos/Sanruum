from __future__ import annotations

from datetime import datetime


def get_current_time() -> str:
    """Return the current time as a formatted string."""
    now: datetime = datetime.now()
    return now.strftime('%H:%M:%S')
