from __future__ import annotations

import sys

from fastapi import FastAPI

from sanruum.ai_system import SanruumAI
from sanruum.app.routes import router as api_router
from sanruum.config.app import HOST
from sanruum.config.app import PORT
from sanruum.database.core.db import init_db
from sanruum.utils.base.logger import logger

app = FastAPI()


def main() -> None:
    """Initialize and run the Sanruum AI system."""
    logger.info('Starting the Sanruum AI system...')  # Log when the system starts
    # Initialize database
    try:
        ai_system = SanruumAI()  # Create an instance of the AI system
        logger.info('Sanruum AI system initialized successfully.')
        ai_system.run()  # Run the AI system
        logger.info('Sanruum AI system is running.')

    except Exception:
        logger.exception(
            'An error occurred while initializing or running the Sanruum AI system',
        )
        sys.exit(1)


if __name__ == '__main__':
    import uvicorn
    from threading import Thread

    # Initialize the database first.
    init_db()

    # Include the API routes before starting the server.
    app.include_router(api_router)

    # Run the AI system in a separate daemon thread.
    Thread(target=main, daemon=True).start()

    logger.info('Sanruum AI System Ready 🚀')
    uvicorn.run(app, host=HOST, port=PORT)
