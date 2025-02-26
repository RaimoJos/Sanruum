from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from sanruum.models.user import User


def get_user(
        db: Session,
        user_id: int,
) -> Any:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Any:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: User) -> object:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_profile(db: Session, user_id: int, profile_data: dict) -> Any:
    user = get_user(db, user_id)
    if user and user.profile:
        for key, value in profile_data.items():
            setattr(user.profile, key, value)
        db.commit()
        db.refresh(user.profile)
    return user
