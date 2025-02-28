from __future__ import annotations

import sys
import traceback

from sanruum.ai_system import SanruumAI
from sanruum.database.core.db import init_db
from sanruum.utils.base.logger import logger


def main() -> None:
    """Initialize and run the Sanruum AI system."""
    logger.info('Starting the Sanruum AI system...')  # Log when the system starts
    # Initialize database
    init_db()
    try:
        ai_system = SanruumAI()  # Create an instance of the AI system
        logger.info('Sanruum AI system initialized successfully.')
        ai_system.run()  # Run the AI system
        logger.info('Sanruum AI system is running.')

    except Exception as e:
        # Capture the full traceback for debugging
        logger.error(f'An error occurred while initializing the AI system: {e}')
        logger.error('Traceback details:')
        logger.error(''.join(traceback.format_exception(None, e, e.__traceback__)))
        sys.exit(1)  # Exit with an error code to signal failure


if __name__ == '__main__':
    main()
