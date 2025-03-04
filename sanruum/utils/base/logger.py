from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

from rich.console import Console
from rich.logging import RichHandler

if TYPE_CHECKING:
    from sanruum.config.base import BaseConfig

console = Console()


class SanruumLogger:
    _instance: SanruumLogger | None = None

    def __new__(cls, *args: object, **kwargs: object) -> SanruumLogger:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self) -> None:
        from sanruum.config.base import BaseConfig
        self.logger = logging.getLogger('sanruum')
        self.logger.setLevel(self._get_log_level())
        self.logger.propagate = False

        if not self.logger.hasHandlers():
            self._setup_console_handler()
            self._setup_file_handler(BaseConfig)

        sys.excepthook = self.log_uncaught_exceptions

    def _setup_console_handler(self) -> None:
        console_handler = RichHandler(console=console, show_time=True, show_path=True)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self, config_class: type[BaseConfig]) -> None:
        log_file = self._get_log_file_path(config_class)
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file, maxBytes=5_000_000, backupCount=3, encoding='utf-8',
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(message)s - '
            'File: %(filename)s - Line: %(lineno)d',
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    @staticmethod
    def _get_log_file_path(config_class: type[BaseConfig]) -> Path:
        env = os.getenv('SANRUUM_ENV', 'development').lower()
        if env == 'production':
            return config_class.LOG_DIR / 'sanruum_prod.log'
        elif env == 'testing':
            return config_class.LOG_DIR / 'sanruum_test.log'
        return config_class.LOG_DIR / 'sanruum_dev.log'

    @staticmethod
    def _get_log_level() -> int:
        log_level = os.getenv('SANRUUM_LOG_LEVEL', 'DEBUG').upper()
        return getattr(logging, log_level, logging.DEBUG)

    def log_uncaught_exceptions(
            self,
            exc_type: type[BaseException],
            exc_value: BaseException,
            exc_traceback: TracebackType | None,
    ) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.logger.critical(
            'Uncaught Exception', exc_info=(
                exc_type, exc_value, exc_traceback,
            ),
        )

    def log_error_with_traceback(self, exception: Exception) -> None:
        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_tb is not None:
            filename = exc_tb.tb_frame.f_code.co_filename
            lineno = exc_tb.tb_lineno
            self.logger.error(
                f'An error occurred: {exception} - File: {filename} - Line: {lineno}',
                exc_info=True,
            )
        else:
            self.logger.error(f'An error occurred: {exception}')


logger = SanruumLogger().logger

if 'PYTEST_CURRENT_TEST' in os.environ or 'pytest' in sys.modules:
    setattr(logger, 'warning', MagicMock())
    setattr(logger, 'error', MagicMock())
