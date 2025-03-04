from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

from sanruum.config import BaseConfig
from sanruum.utils.base.logger import logger


class EnvironmentManager:
    ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
    DEFAULT_ENV = """
SANRUUM_ENV=development
DATABASE_NAME=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_URL_PROD=
SECRET_KEY=
DEBUG=True
LOG_LEVEL=INFO
"""

    @classmethod
    def load_env(cls) -> None:
        if not cls.ENV_PATH.exists():
            cls.ENV_PATH.write_text(cls.DEFAULT_ENV.strip())
            logger.info('.env file created with default values')
        load_dotenv()

    @classmethod
    def update_env(cls) -> None:
        if not cls.ENV_PATH.exists():
            cls.ENV_PATH.write_text(cls.DEFAULT_ENV.strip())

        with cls.ENV_PATH.open('r+') as file:
            content = file.readlines()
            keys = {line.split('=')[0] for line in content if '=' in line}
            new_keys = cls.DEFAULT_ENV.strip().splitlines()

            updated = False
            for line in new_keys:
                key = line.split('=')[0]
                if key not in keys:
                    content.append(f'{line}\n')
                    updated = True

            if updated:
                file.seek(0)
                file.writelines(content)
                file.truncate()
                logger.info('.env updated')

        load_dotenv()


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    f'sqlite:///{BaseConfig.DATA_DIR / "sanruum_dev.db"}'
    LOG_FILE = BaseConfig.LOG_DIR / 'sanruum_dev.log'


class TestingConfig(BaseConfig):
    DEBUG = True
    DB_URL = (
        f'sqlite:///{BaseConfig.DATA_DIR / "sanruum_test.db"}'
    )
    LOG_FILE = BaseConfig.LOG_DIR / 'sanruum_test.log'


class ProductionConfig(BaseConfig):
    DEBUG = False
    f'sqlite:///{BaseConfig.DATA_DIR / "sanruum_prod.db"}'
    LOG_FILE = BaseConfig.LOG_DIR / 'sanruum_prod.log'
