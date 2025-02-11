# sanruum\utils\logger.py
from __future__ import annotations

import io
import logging
import os
import sys
from pathlib import Path

import colorlog

from sanruum.constants import LOG_FILE

# Ensure log directory exists
log_path = Path(LOG_FILE).parent
log_path.mkdir(parents=True, exist_ok=True)

# Ensure UTF-8 output without detaching
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8',
        errors='replace',
    )

# Log format
LOG_FORMAT = (
    '%(asctime)s - [%(levelname)s] - %(message)s '
    '- File: %(filename)s - Line: %(lineno)d'
)
COLOR_FORMAT = (
    '%(log_color)s%(asctime)s - [%(levelname)s] '
    '- %(message)s%(reset)s - File: %(filename)s - Line: %(lineno)d'
)

# Console handler (colored)
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = colorlog.ColoredFormatter(
    COLOR_FORMAT,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
)
console_handler.setFormatter(console_formatter)

# File handler (detailed logs)
file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)

# Logger setup
logger = logging.getLogger('sanruum')

# Use an environment variable for logging level (default to DEBUG)
log_level = os.getenv('SANRUUM_LOG_LEVEL', 'DEBUG').upper()
logger.setLevel(getattr(logging, log_level, logging.DEBUG))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Prevent duplicate log entries if imported multiple times
logger.propagate = False


# Custom error logging with clickable tracebacks (PyCharm)
def log_error_with_traceback(exception: Exception) -> None:
    """Log an error with a full traceback, making it clickable in PyCharm."""
    exc_type, exc_value, exc_tb = sys.exc_info()

    # Check if exc_tb is not None before accessing its attributes
    if exc_tb is not None:
        filename = exc_tb.tb_frame.f_code.co_filename
        lineno = exc_tb.tb_lineno
        logger.error(
            f'An error occurred: {exception} - File: {filename} - Line: {lineno}',
            exc_info=True,
        )
    else:
        # If no traceback exists, log the error without file/line details
        logger.error(f'An error occurred: {exception}')
