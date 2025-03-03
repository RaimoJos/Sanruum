from __future__ import annotations

from typing import Any

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from sanruum.database.core.db import Base


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    token = Column(Text)

    def __init__(self, name: Any, token: Any) -> None:
        self.name = name
        self.token = token
