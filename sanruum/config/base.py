from __future__ import annotations

import os
from pathlib import Path

from sanruum.config.project import ProjectDirectories


class BaseConfig:
    directories = ProjectDirectories(Path(__file__).resolve().parent.parent.parent)
    directories.init_dirs()
    ENV = os.getenv('SANRUUM_ENV', 'development').lower()

    LOG_DIR = directories.LOG_DIR
    LOG_FILE = LOG_DIR / f'sanruum_{ENV}.log'

    DATA_DIR = directories.DATA_DIR

    DB_URL = f"sqlite:///{DATA_DIR / 'sanruum.db'}"
    INTENTS_FILE = directories.INTENTS_DIR / 'intents.json'
    USER_MEMORY_DIR = directories.USER_MEMORY_DIR
    MEMORY_FILE = USER_MEMORY_DIR / 'memory.json'
    SESSION_HISTORY_FILE = DATA_DIR / 'session_history.json'

    PERSONALITY_MODE = 'friendly'  # Options: "formal", "friendly", "professional"

    @classmethod
    def reload(cls) -> None:
        cls.directories = ProjectDirectories(
            Path(__file__).resolve().parent.parent.parent,
        )
        cls.directories.init_dirs()
        cls.ENV = os.getenv('SANRUUM_ENV', 'development').lower()
        cls.LOG_FILE = cls.LOG_DIR / f'sanruum_{cls.ENV}.log'

# Utility functions
# def is_production() -> bool:
#     return BaseConfig.ENV == 'production'
