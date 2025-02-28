from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sanruum.constants import DATABASE_URL
from sanruum.database.core.base import Base

engine = create_engine(
    DATABASE_URL, echo=False, future=True,
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False, autoflush=False, bind=engine,
    ),
)


# Initialize the database
def init_db() -> None:
    """Create database tables."""
    Base.metadata.create_all(bind=engine)
