# sanruum\database\core\db.py
from __future__ import annotations

from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sanruum.config import DATABASE_URL
from sanruum.database.models.core.base import Base

engine = create_engine(DATABASE_URL, echo=True)  # Set echo=False to disable SQL
#                                                  logging in production

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
