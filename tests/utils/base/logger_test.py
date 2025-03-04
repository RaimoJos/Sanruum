from __future__ import annotations

import importlib
import logging
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from sanruum.utils.base.logger import logger
from sanruum.utils.base.logger import SanruumLogger


# Test 1: Check if logger is set up correctly
def test_logger_setup() -> None:
    # Check if the logger has handlers set up
    handlers = logger.handlers
    assert len(handlers) == 2  # Should have 2 handlers: console and file

    # Check if the log level is correct
    assert logger.level == logging.DEBUG  # Default level is DEBUG


# Test 2: Check if the log file exists in the right environment
@pytest.mark.parametrize(
    'env, expected_log_file', [
        ('development', 'sanruum_dev.log'),
        ('production', 'sanruum_prod.log'),
        ('testing', 'sanruum_test.log'),
    ],
)
# Test Function
def test_log_file_path(env: str, expected_log_file: str) -> None:
    with patch.dict('os.environ', {'SANRUUM_ENV': env}):
        import sanruum.utils.base.logger as logger_module
        importlib.reload(logger_module)
        from sanruum.config.base import BaseConfig

        log_file = logger_module.SanruumLogger()._get_log_file_path(BaseConfig)
        assert expected_log_file in str(log_file)


# Test 3: Test error logging with exception
def test_log_error_with_traceback() -> Any:
    try:
        raise ValueError('Test exception')
    except ValueError as e:
        with patch('sanruum.utils.base.logger.logger.error') as mock_error:
            sanruum_logger = SanruumLogger()
            sanruum_logger.log_error_with_traceback(e)
            # Get the actual call arguments
            mock_error.assert_called_once()
            args, kwargs = mock_error.call_args
            log_message = args[0]
            # Check that the log message contains the exception text
            assert 'Test exception' in log_message
            # Optionally, check that the traceback info flag is True
            assert kwargs.get('exc_info') is True


@pytest.mark.parametrize('log_method', ['warning', 'error'])
def test_mock_logger(log_method: str) -> None:
    with patch(
            f'sanruum.utils.base.logger.logger.{log_method}', MagicMock(),
    ) as mock_method:
        logger_method = getattr(logger, log_method)
        logger_method('Test message')
        mock_method.assert_called_once_with('Test message')
