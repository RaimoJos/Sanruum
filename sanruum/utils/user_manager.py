from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from sanruum.database.db import SessionLocal
from sanruum.models.user import User
from sanruum.utils.logger import logger


class UserManager:
    def __init__(self) -> None:
        self.db: Session = SessionLocal()

    def get_user(self, user_id: int) -> User | None:
        """Fetch user by user_id."""
        found_user: User | None = self.db.get(User, user_id)
        return found_user

    def get_user_by_username(self, username: str) -> User | None:
        """Fetch user by username."""
        found_user: User | None = self.db.query(User).filter(
            User.username == username,
        ).first()
        return found_user

    def add_user(self, username: str) -> User | None:
        """Create and add a new user."""
        try:
            new_user = User(username=username)
            with self.db.begin():
                self.db.add(new_user)
                self.db.flush()
            return new_user
        except SQLAlchemyError as e:
            logger.error(f'Error adding user: {e}')
            self.db.rollback()
            return None

    def update_user(
            self,
            user_id: int,
            update_data: dict,
    ) -> User | None:
        """Update user attributes."""
        found_user = self.get_user(user_id)
        if not found_user:
            return None

        try:
            for key, value in update_data.items():
                if hasattr(found_user, key):
                    setattr(found_user, key, value)
            with self.db.begin():
                self.db.flush()
            return found_user
        except SQLAlchemyError as e:
            logger.error(f'Error updating user {user_id}: {e}')
            self.db.rollback()
            return None

    def delete_user(self, user_id: int) -> bool:
        """Delete user by user_id."""
        found_user = self.get_user(user_id)
        if not found_user:
            return False

        try:
            with self.db.begin():
                self.db.delete(found_user)
            return True
        except SQLAlchemyError as e:
            logger.error(f'Error deleting user {user_id}: {e}')
            self.db.rollback()
            return False

    def close(self) -> None:
        """Close database connection."""
        self.db.close()


# Add test user
if __name__ == '__main__':
    user_manager = UserManager()
    user = user_manager.add_user('testuser')
    if user:
        print(f'User added: {user.id}')
