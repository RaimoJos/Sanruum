from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'), index=True)
    action = Column(String)  # e.g., "update_profile", "log_health_record"
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String)  # JSON string or detailed

    user = relationship('User', back_populates='audit_logs')
