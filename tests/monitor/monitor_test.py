# tests\monitor\monitor_test.py
from __future__ import annotations

import subprocess
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from sanruum.constants import BASE_DIR
from sanruum.monitor.monitor import SanruumMonitor


@pytest.fixture
def monitor() -> SanruumMonitor:
    """Fixture for SanruumMonitor"""
    return SanruumMonitor(base_dir=BASE_DIR)


def test_check_project_structure(monitor: SanruumMonitor) -> None:
    """Test if project structure is checked correctly"""
    with (
        patch('os.path.exists', return_value=True),
        patch('os.path.isfile', return_value=True),
    ):
        monitor.check_project_structure()
        # This will test if no missing directories or files will raise warnings.
        # We expect no warnings since mock functions return True
        # (i.e., all required directories and files are found).


def test_run_subprocess_success(monitor: SanruumMonitor) -> None:
    """Test if subprocess runs successfully"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout='Success', stderr='')
        monitor.run_subprocess(['echo', 'test'], 'Echo test')
        mock_run.assert_called_once_with(
            ['echo', 'test'], check=True, capture_output=True, text=True,
        )


def test_run_subprocess_failure(monitor: SanruumMonitor) -> None:
    """Test if subprocess failure is handled correctly"""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, 'echo', 'Error')
        with patch('sanruum.utils.logger.logger.error') as mock_error:
            with pytest.raises(subprocess.CalledProcessError):
                monitor.run_subprocess(['echo', 'fail'], 'Echo fail')
            mock_error.assert_called_with('🚨 Echo fail failed: Error')


def test_check_system_health(monitor: SanruumMonitor) -> None:
    """Test the system health check"""
    with (
        patch('psutil.cpu_percent', return_value=50),
        patch('psutil.virtual_memory', return_value=MagicMock(percent=40)),
        patch('psutil.disk_usage', return_value=MagicMock(percent=30)),
    ):
        with patch('sanruum.utils.logger.logger.info') as mock_info:
            monitor.check_system_health()
            mock_info.assert_any_call('📊 CPU Usage: 50%')
            mock_info.assert_any_call('📊 Memory Usage: 40%')
            mock_info.assert_any_call('📊 Disk Usage: 30%')


def test_run_tests(monitor: SanruumMonitor) -> None:
    """Test if automated tests are run correctly"""
    with patch(
            'sanruum.monitor.monitor.SanruumMonitor.run_subprocess',
    ) as mock_run_subprocess:
        monitor.run_tests()
        mock_run_subprocess.assert_called_once_with(
            ['poetry', 'run', 'pytest', '-v'], 'Pytest',
        )


def test_monitor(monitor: SanruumMonitor) -> None:
    """Test the full monitoring process"""
    with (
        patch('sanruum.monitor.monitor.SanruumMonitor.check_project_structure'),
        patch('sanruum.monitor.monitor.SanruumMonitor.lint_code'),
        patch('sanruum.monitor.monitor.SanruumMonitor.check_dependencies'),
        patch('sanruum.monitor.monitor.SanruumMonitor.check_system_health'),
        patch('sanruum.monitor.monitor.SanruumMonitor.run_tests'),
        patch('sanruum.utils.logger.logger.info') as mock_info,
    ):
        monitor.monitor()
        mock_info.assert_any_call('✅ Monitoring completed successfully!')
