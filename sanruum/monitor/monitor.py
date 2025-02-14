# sanruum/monitor/monitor.py
from __future__ import annotations

import os
import sched
import subprocess
import time

import psutil

from sanruum.constants import BASE_DIR
from sanruum.utils.logger import logger


class SanruumMonitor:
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = base_dir or BASE_DIR  # Use BASE_DIR if not provided
        self.scheduler = sched.scheduler(time.time, time.sleep)
        print(f'Base directory resolved to: {self.base_dir}')  # Debugging output

    def check_project_structure(
            self,
            required_dirs: list[str] | None = None,
            required_files: list[str] | None = None,
    ) -> None:
        print(f'Checking project structure in {self.base_dir}')

        required_dirs = required_dirs or [
            'sanruum',
            'sanruum/ai_core',
            'sanruum/utils',
            'tests',
        ]
        required_files = required_files or ['README.md', '.env']

        # Make sure paths are absolute
        missing_dirs = [
            d for d in required_dirs if not os.path.exists(
                os.path.join(self.base_dir, d),
            )
        ]
        missing_files = [
            f for f in required_files if not os.path.isfile(
                os.path.join(self.base_dir, f),
            )
        ]

        if missing_dirs:
            logger.warning(f"🚨 Missing directories: {', '.join(missing_dirs)}")
        if missing_files:
            logger.warning(f"🚨 Missing files: {', '.join(missing_files)}")
        if not missing_dirs and not missing_files:
            logger.info('✅ Project structure looks good.')

    @staticmethod
    def run_subprocess(command: list, name: str) -> None:
        """Run a subprocess and log the result."""
        try:
            logger.info(f"Running command: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(f'✅ {name} completed successfully.\n{result.stdout}')
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr if e.stderr else (
                e.output if e.output else 'Unknown error'
            )
            logger.error(f'🚨 {name} failed: {err_msg}')
            raise

    @staticmethod
    def check_dependencies() -> None:
        """Check if dependencies are installed properly."""
        logger.info('🔧 Checking dependencies...')
        try:
            result = subprocess.run(
                ['poetry', 'show'],
                check=True,
                capture_output=True,
                text=True,
            )
            if result.stdout:
                logger.info('✅ Dependencies are up to date.')
        except subprocess.CalledProcessError as e:
            logger.error(
                f'🚨 Dependency check failed: {e.stderr.strip()}. Run `poetry install`.',
            )

    @staticmethod
    def check_system_health() -> None:
        """Check CPU, memory, and disk usage."""
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')

        logger.info(f'📊 CPU Usage: {cpu_usage}%')
        logger.info(f'📊 Memory Usage: {memory_info.percent}%')
        logger.info(f'📊 Disk Usage: {disk_usage.percent}%')

        if cpu_usage > 90:
            logger.warning('🚨 High CPU usage detected!')
        if memory_info.percent > 85:
            logger.warning('🚨 High memory usage detected!')
        if disk_usage.percent > 90:
            logger.warning('🚨 Disk space is critically low!')

    def run_tests(self) -> None:
        """Run automated tests."""
        logger.info('🔍 Running tests...')
        try:
            self.run_subprocess(['poetry', 'run', 'pytest', '-v'], 'Pytest')
        except subprocess.CalledProcessError as e:
            logger.error(f'❌ Pytest failed with output:\n{e.stderr}')

    def lint_code(self) -> None:
        """Run code linting."""
        logger.info('🔍 Running linting...')
        self.run_subprocess(['poetry', 'run', 'flake8', self.base_dir], 'Lint')

    def monitor(self) -> None:
        """Run all system checks."""
        logger.info('🔄 Running full system monitoring...')
        try:
            self.check_project_structure()
            self.check_dependencies()
            self.check_system_health()
            self.run_tests()
            logger.info('✅ Monitoring completed successfully!')
        except Exception as e:
            logger.error(f'❌ Monitoring encountered an error: {e}')


if __name__ == '__main__':
    monitor = SanruumMonitor('.')
