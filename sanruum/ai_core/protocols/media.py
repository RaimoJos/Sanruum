from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import HealthMediaID
from custom_types import UserID


class HealthMediaProtocol(Protocol):
    id: HealthMediaID
    user_id: UserID
    media_type: str  # e.g., "photo", "scan", "video"
    file_path: str
    timestamp: datetime
    description: str | None
