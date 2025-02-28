from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.core.base import Base


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'), index=True)
    action = Column(String)  # e.g., "update_profile", "log_health_record"
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String)  # JSON string or detailed

    user = relationship('User', back_populates='audit_logs')
