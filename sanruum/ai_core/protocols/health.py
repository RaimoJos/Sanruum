from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import BloodPressure
from custom_types import BloodSugar
from custom_types import DiseaseID
from custom_types import Weight


class HealthRecordProtocol(Protocol):
    timestamp: datetime
    blood_sugar: BloodSugar | None
    weight: Weight | None
    blood_pressure: BloodPressure | None
    heart_rate: int | None
    cholesterol: float | None
    triglycerides: float | None
    sleep_duration: float | None


class DiseaseProtocol(Protocol):
    id: DiseaseID
    name: str  # Disease name
    icd_code: str | None  # ICD classification (optional)
    description: str
    category: str | None  # e.g., "metabolic", "cardiovascular", etc.


class HydrationProtocol(Protocol):
    # TODO: Add Hydration...
    pass


class StressProtocol(Protocol):
    # TODO: Add Stress...
    pass


class SymptomsCheckProtocol(Protocol):
    # TODO: Add SymptomsCheck...
    pass
