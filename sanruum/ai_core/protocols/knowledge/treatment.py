from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import DoctorVisitID
from custom_types import MedicalHistoryID
from custom_types import MedicationID
from custom_types import TreatmentID
from custom_types import UserID
from custom_types import UserMedicationID


class TreatmentProtocol(Protocol):
    id: TreatmentID
    user_id: UserID
    treatment_type: str  # e.g., "surgery", "therapy", "lifestyle change"
    start_date: datetime
    end_date: datetime | None


class MedicalHistoryProtocol(Protocol):
    id: MedicalHistoryID
    user_id: UserID
    condition: str  # e.g., "hypertension", "asthma"
    diagnosis_date: datetime
    notes: str | None  # Additional details about the condition


class UserMedicationProtocol(Protocol):
    id: UserMedicationID
    user_id: UserID
    medication_id: MedicationID
    dosage: str  # e.g., "500 mg", "10 units"
    schedule: str  # e.g, "8 AM and 8 PM"
    start_date: datetime
    end_date: datetime | None


class DoctorVisitProtocol(Protocol):
    id: DoctorVisitID
    user_id: UserID
    visit_date: datetime
    doctor_name: str | None
    diagnosis: str | None
    recommendations: str | None
    follow_up_date: datetime | None
    notes: str | None


class MedicationProtocol(Protocol):
    id: MedicationID
    name: str
    description: str
    route: str | None  # e.g., "oral", "injection", "topical"
    frequency: str | None  # e.g., "daily", "twice a day"
    side_effects: str | None
    interactions: str | None
