from __future__ import annotations

from datetime import datetime
from typing import Protocol

from custom_types import FoodID
from custom_types import MealLogID
from custom_types import UserID


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
