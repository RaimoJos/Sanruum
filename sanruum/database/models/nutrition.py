from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    calories = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    description = Column(String, nullable=True)


class MealLog(Base):
    __tablename__ = 'meal_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    total_calories = Column(Float, nullable=True)
    total_carbs = Column(Float, nullable=True)
    total_protein = Column(Float, nullable=True)
    total_fat = Column(Float, nullable=True)

    user = relationship('User', back_populates='meal_log')
