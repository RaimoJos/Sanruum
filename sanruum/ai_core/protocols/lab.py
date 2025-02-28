from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import LabTestID
from custom_types import UserID


class LabTestProtocol(Protocol):
    id: LabTestID
    user_id: UserID
    test_name: str  # e.g., "HbA1c", "Cholesterol", etc.
    result: float | None  # The test result value (may be None if pending)
    unit: str | None  # e.g., "%", "mmol/L", "mg/dL"
    reference_range: str | None  # e.g., "4.0-5.6"
    test_date: datetime
    notes: str | None  # Additional information (e.g., fasting status)
