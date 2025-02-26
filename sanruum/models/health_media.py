from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class HealthMedia(Base):
    tablename = 'health_media'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    media_type = Column(String)  # e.g., "photo", "scan", "video"
    file_path = Column(String)  # path or URL to the media file
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=True)

    user = relationship('User', back_populates='health_media')
