from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.core.base import Base


class Treatment(Base):
    __tablename__ = 'treatments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    treatment_type = Column(String)  # e.g., "surgery", "therapy", "lifestyle change"
    description = Column(String)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    user = relationship('User', back_populates='treatments')
