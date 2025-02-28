from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import MoodLogID
from custom_types import UserID


class MoodLogProtocol(Protocol):
    id: MoodLogID
    user_id: UserID
    timestamp: datetime
    mood: str  # e.g., "happy", "anxious", "stressed"
    stress_level: float | None  # Scale 0-10
    notes: str | None  # Additional comments
