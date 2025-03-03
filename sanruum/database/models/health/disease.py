from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sanruum.database.core.db import Base
from sanruum.database.models.core.user import user_diseases


class Disease(Base):
    __tablename__ = 'diseases'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # ICD code for standardized classification.
    icd_code = Column(String, nullable=True)
    description = Column(String)
    # e.g., "metabolic", "cardiovascular", etc.
    category = Column(String, nullable=True)

    users = relationship('User', secondary=user_diseases, back_populates='diseases')
