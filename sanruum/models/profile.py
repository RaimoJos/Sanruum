from __future__ import annotations

from typing import Any

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    age = Column(Integer)
    weight = Column(Float)  # in kg
    height = Column(Float)  # in cm
    # e.g., "Type 1", "Type 2", or None for healthy individuals
    diabetes_type = Column(String)
    goal = Column(String)  # e.g., "weight loss", "healthy lifestyle", etc

    # Personalized settings for for diabetes management(if applicable)
    insulin_to_carb_ratio = Column(Float, default=10.0)
    correction_factor = Column(Float, default=2.0)
    target_bg = Column(Float, default=5.5)

    # Carbs
    meal_carb_range_low = Column(Integer, default=45)
    meal_carb_range_high = Column(Integer, default=60)
    snack_carb_range_low = Column(Integer, default=15)
    snack_carb_range_high = Column(Integer, default=30)

    # Additional lifestyle preferences...(exercise frequency, dietary preferences, etc.)

    user = relationship('User', back_populates='profile')
