from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.core.db import Base


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    diabetes_type = Column(String)
    goal = Column(String)
    insulin_to_carb_ratio = Column(Float, default=10.0)
    correction_factor = Column(Float, default=2.0)
    target_bg = Column(Float, default=5.5)
    timezone = Column(String, default='Europe/Tallinn')
    meal_carb_range_low = Column(Integer, default=45)
    meal_carb_range_high = Column(Integer, default=60)
    snack_carb_range_low = Column(Integer, default=15)
    snack_carb_range_high = Column(Integer, default=30)

    user = relationship('User', back_populates='profile')
