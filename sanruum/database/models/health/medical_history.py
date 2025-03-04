from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.models.core.base import Base


class MedicalHistory(Base):
    __tablename__ = 'medical_history'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    condition = Column(String)  # e.g., "hypertension", "asthma"
    diagnosis_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)

    user = relationship('user', back_populates='medical_history')
