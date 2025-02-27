from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()

# Many-to-many association table for users and diseases
user_diseases = Table(
    'user_diseases',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('disease_id', Integer, ForeignKey('diseases.id'), primary_key=True),
    Column('diagnosis_date', DateTime, default=datetime.utcnow),
    Column('severity', String),  # e.g., mild, moderate, severe
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    profile = relationship(
        'UserProfile',
        back_populates='user',
        uselist=False,
        lazy='joined', )
    health_record = relationship(
        'HealthRecord',
        back_populates='user',
        cascade='all, delete-orphan', )
    diseases = relationship(
        'Disease',
        secondary=user_diseases,
        back_populates='users',
        lazy='subquery', )
    user_medications = relationship(
        'UserMedication',
        back_populates='user',
        cascade='all, delete-orphan', )
    health_media = relationship(
        'HealthMedia',
        back_populates='user',
        cascade='all, delete-orphan', )
    treatments = relationship(
        'Treatments',
        back_populates='user',
        cascade='all, delete-orphan', )
    meal_logs = relationship(
        'MealLog',
        back_populates='user',
        cascade='all, delete-orphan', )
    activity_logs = relationship(
        'ActivityLog',
        back_populates='user',
        cascade='all, delete-orphan', )
    consents = relationship(
        'Consents',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    audit_log = relationship(
        'AuditLog',
        back_populates='user',
        cascade='all, delete-orphan', )
    lab_tests = relationship(
        'LabTest',
        back_populates='user',
        cascade='all, delete-orphan', )
    doctor_visits = relationship(
        'DoctorVisit',
        back_populates='user',
        cascade='all, delete-orphan', )
    mood_logs = relationship(
        'MoodLog',
        back_populates='user',
        cascade='all, delete-orphan', )
    medical_history = relationship(
        'MedicalHistory',
        back_populates='user',
        cascade='all, delete-orphan', )
