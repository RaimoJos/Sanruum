from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.models.core.base import Base


class DoctorVisit(Base):
    __tablename__ = 'doctor_visits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    visit_date = Column(DateTime, default=datetime.utcnow)
    doctor_name = Column(String, nullable=True)
    diagnosis = Column(String, nullable=True)
    recommendations = Column(String, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)

    user = relationship('User', back_populates='doctor_visits')
