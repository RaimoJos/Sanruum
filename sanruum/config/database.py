# sanruum/config/database.py
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(var_name: str, default: str | None = None) -> str:
    value = os.getenv(var_name, default)
    if value is None:
        raise OSError(f'Set the {var_name} environment variable')
    return value


dbname = os.getenv('DATABASE_NAME')
db_host = os.getenv('DATABASE_HOST', 'localhost')
db_port = os.getenv('DATABASE_PORT', '5432')
db_user = os.getenv('DATABASE_USERNAME')
db_password = os.getenv('DATABASE_PASSWORD')

DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{dbname}'
