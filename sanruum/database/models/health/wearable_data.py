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


class WearableData(Base):
    __tablename__ = 'wearable_data'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    heart_rate = Column(Float, nullable=True)
    steps = Column(Integer, nullable=True)
    sleep_quality = Column(Float, nullable=True)  # e.g., a "score" or "duration"
    # e.g., "light", "moderate", "intense"
    activity_level = Column(String, nullable=True)

    user = relationship('User', back_populates='')
