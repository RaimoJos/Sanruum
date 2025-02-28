from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.core.base import Base


class UserConsent(Base):
    __tablename__ = 'user_consents'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    consent_type = Column(String)  # e.g., "data_sharing", "research_usage"
    consent_given = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='consents')
