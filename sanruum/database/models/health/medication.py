from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.core.db import Base


class Medication(Base):
    __tablename__ = 'medications'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    route = Column(String, nullable=True)  # e.g., oral, injection, topical.
    frequency = Column(String, nullable=True)  # e.g., "daily", "twice a day".
    side_effects = Column(String, nullable=True)
    interactions = Column(String, nullable=True)

    user_medications = relationship('UserMedication', back_populates='medication')


class UserMedication(Base):
    __tablename__ = 'user_medications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    medication_id = Column(Integer, ForeignKey('medications.id'), index=True)
    dosage = Column(String)  # e.g., "500 mg", "10 units"
    schedule = Column(String)  # e.g, "8 AM and 8 PM"
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    user = relationship('User', back_populates='user_medications')
    medication = relationship('Medication', back_populates='user_medications')
