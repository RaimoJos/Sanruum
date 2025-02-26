from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from typing import NewType

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


@dataclass
class BloodPressure:
    systolic: BloodPressureValue
    diastolic: BloodPressureValue
