from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.core.db import Base


class MoodLog(Base):
    __tablename__ = 'mood_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    mood = Column(String)  # e.g., "happy", "anxious", "stressed"
    stress_level = Column(Float, nullable=True)  # on a scale, e.g, 0-10
    notes = Column(String, nullable=True)

    user = relationship('User', back_populates='mood_logs')
