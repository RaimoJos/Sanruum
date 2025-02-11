# sanruum\main.py
from __future__ import annotations

import logging

from sanruum.ai_system import SanruumAI

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Initialize and run the Sanruum AI system."""
    try:
        ai_system = SanruumAI()  # Create an instance of the AI system
        ai_system.run()  # Run the AI system
    except Exception as e:
        logger.error(f'An error occurred while running the AI system: {e}')


if __name__ == '__main__':
    main()
