from __future__ import annotations

from fastapi_admin.models import AbstractAdmin
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sanruum.database.core.db import Base


class AdminUser(Base, AbstractAdmin):
    __tablename__ = 'admin_users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)

    def __str__(self) -> Column[str]:
        return self.username
