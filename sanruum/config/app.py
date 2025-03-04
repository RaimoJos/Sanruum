from __future__ import annotations

import os

HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 5000))
SECRET_KEY = os.getenv('SECRET_KEY')
LOCAL_ADDRESS = f'https://{HOST}:{PORT}'
