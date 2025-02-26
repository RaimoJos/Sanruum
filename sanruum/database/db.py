from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sanruum.constants import DATABASE_PATH

engine = create_engine(
    f'sqlite:///{DATABASE_PATH}', connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Initialize the database
def init_db() -> None:
    """Create database tables."""
    from sanruum.database.base import Base

    Base.metadata.create_all(bind=engine)
