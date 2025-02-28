from __future__ import annotations

from typing import Any
from typing import cast
from typing import TypeVar

from sqlalchemy.orm import Session

from sanruum.database.core.base import Base
from sanruum.database.models.core.user import User

T = TypeVar('T', bound=Base)  # Generic Type for SQLAlchemy Models


def get_user(db: Session, user_id: int) -> User | None:
    """Fetch a user by ID."""
    return cast(User | None, db.query(User).filter(User.id == user_id).first())


class Repository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get(self, model: type[T], obj_id: int) -> T | None:
        return cast(T | None, self.db.query(model).filter(model.id == obj_id).first())

    def get_all(self, model: type[T]) -> list[T]:
        return cast(list[T], self.db.query(model).all())

    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: T, **kwargs: dict[str, Any]) -> T:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self.db.delete(obj)
        self.db.commit()
