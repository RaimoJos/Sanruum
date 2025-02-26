from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class HealthRecord(Base):
    __tablename__ = 'health_records'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow())

    # Health metrics
    blood_sugar = Column(Float, nullable=True)  # mmol/L
    weight = Column(Float, nullable=True)  # kg
    systolic_bp = Column(Integer, nullable=True)
    diastolic_bp = Column(Integer, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    cholesterol = Column(Float, nullable=True)
    triglycerides = Column(Float, nullable=True)
    sleep_duration = Column(Float, nullable=True)  # hours
    # hba1c
    # oxygen_saturation

    # additional metrics...

    user = relationship('User', back_populates='health_records')
