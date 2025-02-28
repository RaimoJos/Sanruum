from __future__ import annotations

from datetime import datetime
from typing import Protocol


class WearableDataProtocol(Protocol):
    timestamp: datetime
    heart_rate: float | None
    steps: int | None
    sleep_quality: float | None  # e.g., a score or duration
    activity_level: str | None  # e.g., "light", "moderate", "intense"
