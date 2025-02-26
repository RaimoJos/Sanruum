from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DB_URL = 'sqlite:///data/sanruum.db'

engine = create_engine(
    SQL_ALCHEMY_DB_URL, connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
