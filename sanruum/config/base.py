from __future__ import annotations

import os
from pathlib import Path

from sanruum.config.project import ProjectDirectories


class BaseConfig:
    ENV_CHOICES = ['development', 'testing', 'production']

    @classmethod
    def is_production(cls) -> bool:
        return cls.get_env() == 'production'

    @classmethod
    def is_testing(cls) -> bool:
        return cls.get_env() == 'testing'

    directories = ProjectDirectories(Path(__file__).resolve().parent.parent.parent)
    directories.init_dirs()

    _env: str = os.getenv('SANRUUM_ENV', 'development').lower()

    @classmethod
    def get_env(cls) -> str:
        return cls._env

    @classmethod
    def set_env(cls, env: str) -> None:
        env = env.lower()
        if env not in cls.ENV_CHOICES:
            raise ValueError(f'Invalid environment: {env}')
        cls._env = env
        cls.LOG_FILE = cls.LOG_DIR / f'sanruum_{cls._env}.log'
        from sanruum.utils.base.logger import logger
        logger.info(f'Environment switched to: {env}')

    LOG_DIR: Path = directories.LOG_DIR
    LOG_FILE: Path = LOG_DIR / f'sanruum_{_env}.log'
    DATA_DIR: Path = directories.DATA_DIR

    DB_URL = f"sqlite:///{DATA_DIR / 'sanruum.db'}"
    INTENTS_FILE = directories.INTENTS_DIR / 'intents.json'
    USER_MEMORY_DIR = directories.USER_MEMORY_DIR
    MEMORY_FILE = USER_MEMORY_DIR / 'memory.json'
    SESSION_HISTORY_FILE = DATA_DIR / 'session_history.json'

    PERSONALITY_MODE = 'friendly'  # Options: "formal", "friendly", "professional"

    def reload(self) -> None:
        self.directories = ProjectDirectories(
            Path(__file__).resolve().parent.parent.parent,
        )
        self.directories.init_dirs()
        self.set_env(os.getenv('SANRUUM_ENV', 'development'))
