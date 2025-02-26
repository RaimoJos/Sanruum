from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import AuditLogID
from custom_types import BloodPressure
from custom_types import BloodSugar
from custom_types import ConsentID
from custom_types import DiabetesType
from custom_types import DiseaseID
from custom_types import DoctorVisitID
from custom_types import FoodID
from custom_types import GoalType
from custom_types import HealthMediaID
from custom_types import LabTestID
from custom_types import MealLogID
from custom_types import MedicalHistoryID
from custom_types import MedicationID
from custom_types import MoodLogID
from custom_types import TreatmentID
from custom_types import UserID
from custom_types import UserMedicationID
from custom_types import Weight


# ------------------------------
# HEALTH & USER PROTOCOLS
# ------------------------------
class HealthRecordProtocol(Protocol):
    timestamp: datetime
    blood_sugar: BloodSugar | None  # mmol/L; may be None
    weight: Weight | None  # kg; may be None
    blood_pressure: BloodPressure | None  # kg
    heart_rate: int | None  # beats per minute; may be None
    cholesterol: float | None  # unit depends on context; may be None
    triglycerides: float | None  # may be None
    sleep_duration: float | None  # hours; may be None


class UserProfileProtocol(Protocol):
    timezone: str
    age: int
    weight: float
    height: float
    diabetes_type: DiabetesType | None  # e.g., "Type 1", "Type 2", or None
    goal: GoalType | None  # e.g., "weight loss", "healthy lifestyle", etc.
    insulin_to_carb_ratio: float
    correction_factor: float
    target_bg: float  # target blood glucose in mmol/L
    meal_carb_range_low: int
    meal_carb_range_high: int
    snack_carb_range_low: int
    snack_carb_range_high: int


class UserProtocol(Protocol):
    id: UserID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    profile: UserProfileProtocol | None


# ------------------------------
# WEARABLE DATA PROTOCOL
# ------------------------------
class WearableDataProtocol(Protocol):
    timestamp: datetime
    heart_rate: float | None
    steps: int | None
    sleep_quality: float | None  # e.g., a score or duration
    activity_level: str | None  # e.g., "light", "moderate", "intense"


# ------------------------------
# NUTRITION & FOOD PROTOCOLS
# ------------------------------
class FoodItemProtocol(Protocol):
    id: FoodID
    name: str
    calories: float
    carbs: float
    protein: float
    fat: float
    description: str | None


class MealLogProtocol(Protocol):
    id: MealLogID
    user_id: UserID | None
    timestamp: datetime
    meal_type: str  # e.g., "breakfast", "lunch", "dinner", "snack"
    total_calories: float | None
    total_carbs: float | None
    total_protein: float | None
    total_fat: float | None


# ------------------------------
# TREATMENT PROTOCOLS
# ------------------------------
class TreatmentProtocol(Protocol):
    id: TreatmentID
    user_id: UserID
    treatment_type: str  # e.g., "surgery", "therapy", "lifestyle change"
    start_date: datetime
    end_date: datetime | None


# ------------------------------
# AUDIT LOG PROTOCOL
# ------------------------------
class AuditLogProtocol(Protocol):
    id: AuditLogID
    user_id: UserID
    action: str  # e.g., "update_profile", "log_health_record"
    timestamp: datetime
    details: str | None  # JSON string or additional details


# ------------------------------
# USER CONSENT PROTOCOL
# ------------------------------
class UserConsent(Protocol):
    id: ConsentID
    user_id: UserID
    consent_type: str  # e.g., "data_sharing", "research_usage"
    consent_given: bool
    timestamp: datetime


# ------------------------------
# DISEASE PROTOCOL
# ------------------------------
class DiseaseProtocol(Protocol):
    id: DiseaseID
    name: str  # Disease name
    icd_code: str | None  # ICD classification (optional)
    description: str
    category: str | None  # e.g., "metabolic", "cardiovascular", etc.


# ------------------------------
# DOCTOR VISIT PROTOCOL
# ------------------------------
class DoctorVisitProtocol(Protocol):
    id: DoctorVisitID
    user_id: UserID
    visit_date: datetime
    doctor_name: str | None
    diagnosis: str | None
    recommendations: str | None
    follow_up_date: datetime | None
    notes: str | None


# ------------------------------
# HEALTH MEDIA PROTOCOL
# ------------------------------
class HealthMediaProtocol(Protocol):
    id: HealthMediaID
    user_id: UserID
    media_type: str  # e.g., "photo", "scan", "video"
    file_path: str
    timestamp: datetime
    description: str | None


# ------------------------------
# LAB TEST PROTOCOL
# ------------------------------
class LabTestProtocol(Protocol):
    id: LabTestID
    user_id: UserID
    test_name: str  # e.g., "HbA1c", "Cholesterol", etc.
    result: float | None  # The test result value (may be None if pending)
    unit: str | None  # e.g., "%", "mmol/L", "mg/dL"
    reference_range: str | None  # e.g., "4.0-5.6"
    test_date: datetime
    notes: str | None  # Additional information (e.g., fasting status)


# ------------------------------
# MEDICAL HISTORY PROTOCOL
# ------------------------------
class MedicalHistoryProtocol(Protocol):
    id: MedicalHistoryID
    user_id: UserID
    condition: str  # e.g., "hypertension", "asthma"
    diagnosis_date: datetime
    notes: str | None  # Additional details about the condition


# ------------------------------
# MEDICATION PROTOCOL
# ------------------------------
class MedicationProtocol(Protocol):
    id: MedicationID
    name: str
    description: str
    route: str | None  # e.g., "oral", "injection", "topical"
    frequency: str | None  # e.g., "daily", "twice a day"
    side_effects: str | None
    interactions: str | None


# ------------------------------
# USER MEDICATION PROTOCOL
# ------------------------------
class UserMedicationProtocol(Protocol):
    id: UserMedicationID
    user_id: UserID
    medication_id: MedicationID
    dosage: str  # e.g., "500 mg", "10 units"
    schedule: str  # e.g, "8 AM and 8 PM"
    start_date: datetime
    end_date: datetime | None


# ------------------------------
# MOOD LOG PROTOCOL
# ------------------------------
class MoodLogProtocol(Protocol):
    id: MoodLogID
    user_id: UserID
    timestamp: datetime
    mood: str  # e.g., "happy", "anxious", "stressed"
    stress_level: float | None  # Scale 0-10
    notes: str | None  # Additional comments
