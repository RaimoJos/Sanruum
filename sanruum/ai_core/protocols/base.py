from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import AuditLogID
from custom_types import ConsentID
from custom_types import DiabetesType
from custom_types import GoalType
from custom_types import UserID


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


class UserConsent(Protocol):
    id: ConsentID
    user_id: UserID
    consent_type: str  # e.g., "data_sharing", "research_usage"
    consent_given: bool
    timestamp: datetime


class AuditLogProtocol(Protocol):
    id: AuditLogID
    user_id: UserID
    action: str  # e.g., "update_profile", "log_health_record"
    timestamp: datetime
    details: str | None  # JSON string or additional details
