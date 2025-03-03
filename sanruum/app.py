from __future__ import annotations

import os

from flask import Flask

from sanruum.database.core.db import Base
from sanruum.database.core.db import engine

HOST = 'localhost'
PORT = 5000
LOCAL_ADDRESS = f'https://{HOST}:{PORT}'
SECRET_KEY = os.getenv('SECRET_KEY')

Base.metadata.create_all(bind=engine)
app = Flask(__name__)

# run app
if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', host=HOST, port=PORT)
