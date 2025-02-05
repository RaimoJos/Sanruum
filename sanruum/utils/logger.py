# sanruum\utils\logger.py
import io
import logging
import sys

import colorlog

from sanruum.constants import LOG_FILE

# Ensure UTF-8 output without detaching
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Log format
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(message)s"
COLOR_FORMAT = "%(log_color)s%(asctime)s - [%(levelname)s] - %(message)s%(reset)s"

# Console handler (colored)
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = colorlog.ColoredFormatter(
    COLOR_FORMAT,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red"
    },
)
console_handler.setFormatter(console_formatter)

# File handler (detailed logs)
file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)

# Logger setup
logger = logging.getLogger("sanruum")
logger.setLevel(logging.DEBUG)  # Change to WARNING or INFO in production
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Prevent duplicate log entries if imported multiple times
logger.propagate = False
