from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ENV = os.getenv('SANRUUM_ENV', 'development').lower()


class BaseConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR / 'logs'
    DATA_DIR = BASE_DIR / 'data'
    PROJECT_PATH = BASE_DIR / 'sanruum'
    NLP_DIR = PROJECT_PATH / 'nlp'
    MODEL_DIR = BASE_DIR / 'models'
    NLP_DATA_DIR = NLP_DIR / 'data'
    RAW_TEXT_DATA_DIR = NLP_DATA_DIR / 'raw_data'
    PROCESSED_DATA_DIR = NLP_DATA_DIR / 'processed_data'
    MEMORY_DIR = DATA_DIR / 'memory'
    USER_MEMORY_DIR = MEMORY_DIR / 'user_memory'
    MEMORY_FILE = USER_MEMORY_DIR / 'memory.json'
    INTENTS_DIR = DATA_DIR / 'intents'
    DB_URL = f"sqlite:///{DATA_DIR / 'sanruum.sqlite'}"
    LOG_FILE = LOG_DIR / 'sanruum.log'
    INTENTS_FILE = DATA_DIR / 'intents.json'
    PERSONALITY_MODE = 'friendly'  # Options: "formal", "friendly", "professional"
    SESSION_HISTORY_FILE = DATA_DIR / 'session_history.json'

    @classmethod
    def init_dirs(cls) -> None:
        directories = [
            cls.DATA_DIR, cls.LOG_DIR, cls.NLP_DIR, cls.MODEL_DIR,
            cls.NLP_DATA_DIR, cls.RAW_TEXT_DATA_DIR, cls.PROCESSED_DATA_DIR,
            cls.USER_MEMORY_DIR, cls.INTENTS_DIR,
        ]
        for directory in directories:
            if not directory.exists():
                directory.mkdir(parents=True)
                print(f'Created directory: {directory}')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DB_URL = f"sqlite:///{BaseConfig.DATA_DIR / 'sanruum_dev.sqlite'}"
    LOG_FILE = BaseConfig.LOG_DIR / 'sanruum_dev.log'


class TestingConfig(BaseConfig):
    DEBUG = True
    DB_URL = f"sqlite:///{BaseConfig.DATA_DIR / 'sanruum_test.sqlite'}"
    LOG_FILE = BaseConfig.LOG_DIR / 'sanruum_test.log'


class ProductionConfig(BaseConfig):
    DEBUG = False
    DB_URL = os.getenv('DATABASE_URL_PROD', BaseConfig.DB_URL)
    LOG_FILE = BaseConfig.LOG_DIR / 'sanruum_prod.log'


config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

# Fix for type annotation issue
Config: type[BaseConfig] = config_map.get(ENV, DevelopmentConfig)
Config.init_dirs()


# Utility functions
def is_production() -> bool:
    return ENV == 'production'


print(f'Running in {ENV} mode')


# Utility function to update the .env file
def update_env_file() -> Path | None:
    env_path = BaseConfig.BASE_DIR / '.env'

    # Default environment variables content
    env_content = """
SANRUUM_ENV=development
DATABASE_URL_PROD=  # Set your production DB URL here
SECRET_KEY=  # Set your secret key here
DEBUG=True
LOG_LEVEL=INFO
"""

    # Read existing .env file content
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(env_content)
        print('.env file created with default values')
        return env_path

    # Read current content of the .env file
    with open(env_path, 'r+') as f:
        content = f.readlines()

        # Convert current content to a set of keys
        existing_vars = {line.split('=')[0].strip() for line in content if '=' in line}

        # Default variables we want to make sure are in the file
        new_vars = env_content.strip().splitlines()

        # Add missing environment variables to the file content
        updated = False
        for line in new_vars:
            key = line.split('=')[0]
            if key not in existing_vars:
                content.append(f'{line}\n')
                existing_vars.add(key)  # Add to the set to prevent duplicates
                updated = True
                print(f'Added {line} to .env')

        # Only write the updated content back to the file if it was changed
        if updated:
            f.seek(0)
            f.writelines(content)
            f.truncate()
            print('.env file updated')

    # Return the env_path for later use if necessary
    return env_path


# Ensure that the environment variables are loaded correctly after updating
env_path = update_env_file()
load_dotenv()  # Reload to ensure the updates are applied

if env_path:
    print(f'Does .env exist? {env_path.exists()}')
else:
    print('No .env path returned')
print(f"SANRUUM_ENV: {os.getenv('SANRUUM_ENV')}")
print(f"DATABASE_URL_PROD: {os.getenv('DATABASE_URL_PROD')}")
