from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from typing import NewType
from typing import Union

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

UserID = NewType('UserID', int)
FoodID = NewType('FoodID', int)
MealLogID = NewType('MealLogID', int)
TreatmentID = NewType('TreatmentID', int)
AuditLogID = NewType('AuditLogID', int)
ConsentID = NewType('ConsentID', int)
DiseaseID = NewType('DiseaseID', int)
DoctorVisitID = NewType('DoctorVisitID', int)
HealthMediaID = NewType('HealthMediaID', int)
LabTestID = NewType('LabTestID', int)
MedicalHistoryID = NewType('MedicalHistoryID', int)
MedicationID = NewType('MedicationID', int)
UserMedicationID = NewType('UserMedicationID', int)
MoodLogID = NewType('MoodLogID', int)

BloodSugar = NewType('BloodSugar', float)  # in mmol/L
Weight = NewType('Weight', float)  # in kg
BloodPressureValue = NewType('BloodPressureValue', int)  # mmHg

DiabetesType = Literal['Type 1', 'Type2', None]
GoalType = Literal['weight loss', 'healthy lifestyle', 'maintenance', None]

ENGINE_TYPE = Union[Engine, AsyncEngine]
SESSION_TYPE = Union[Session, AsyncSession]


@dataclass
class BloodPressure:
    systolic: BloodPressureValue
    diastolic: BloodPressureValue
