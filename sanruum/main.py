from __future__ import annotations

import sys

from fastapi import FastAPI

from sanruum.ai_system import SanruumAI
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
    logger.info('Sanruum AI System Ready 🚀')
    main()
