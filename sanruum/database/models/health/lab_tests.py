from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.models.core.base import Base


class LabTest(Base):
    __tablename__ = 'lab_tests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    test_name = Column(String, index=True)  # e.g., "HbA1c", "Cholesterol", etc.
    result = Column(Float, nullable=True)
    unit = Column(String, nullable=True)  # e.g., "%", "mmol/L", "mg/dL"
    reference_range = Column(String, nullable=True)  # e.g., "4.0-5.6"
    test_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)

    user = relationship('User', back_populates='lab_tests')
