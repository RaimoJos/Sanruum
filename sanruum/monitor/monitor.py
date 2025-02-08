from __future__ import annotations

import os
import sched
import subprocess
import time

import psutil

from sanruum.utils.logger import logger


class SanruumMonitor:
    def __init__(self, base_dir: str) -> None:
        self.base_dir = base_dir
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def check_project_structure(
            self,
            required_dirs: list[str] | None = None,
            required_files: list[str] | None = None,
    ) -> None:
        required_dirs = required_dirs or [
            'sanruum',
            'sanruum/ai_core',
            'sanruum/utils',
            'tests',
        ]
        required_files = required_files or ['README.md', 'setup.py', '.env']

        missing_dirs = [
            d
            for d in required_dirs
            if not os.path.exists(os.path.join(self.base_dir, d))
        ]
        missing_files = [
            f
            for f in required_files
            if not os.path.isfile(os.path.join(self.base_dir, f))
        ]

        if missing_dirs:
            logger.warning(
                f"🚨 Missing directories: {', '.join(missing_dirs)}",
            )
        if missing_files:
            logger.warning(f"🚨 Missing files: {', '.join(missing_files)}")
        if not missing_dirs and not missing_files:
            logger.info('✅ Project structure looks good.')

    def run_subprocess(self, command: list[str]) -> None:
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f'🚨 Error while running command: {e.cmd}')
            logger.error(f'Error message: {e.stderr}')
            raise

    def lint_code(self) -> None:
        """Run code formatters and linters."""
        logger.info('🛠 Running code format checks...')
        subprocess.run(['poetry', 'run', 'black', self.base_dir], check=False)
        subprocess.run(['isort', self.base_dir], check=False)
        subprocess.run(['flake8', self.base_dir], check=False)

    def check_dependencies(self) -> None:
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
            else:
                logger.info('✅ Dependencies are up to date.')
        except subprocess.CalledProcessError as e:
            logger.error(
                f'🚨 Dependency check failed: {e.stderr}. Run `poetry install`.',
            )

    def check_system_health(self) -> None:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        logger.info(f'CPU Usage: {cpu_usage}%')
        logger.info(f'Memory Usage: {memory_info.percent}%')
        logger.info(f'Disk Usage: {disk_usage.percent}%')
        if cpu_usage > 90:
            logger.warning('🚨 CPU usage is too high!')
        if memory_info.percent > 85:
            logger.warning('🚨 Memory usage is too high!')
        if disk_usage.percent > 90:
            logger.warning('🚨 Disk usage is too high!')

    @staticmethod
    def run_tests() -> None:
        """Run automated tests."""
        logger.info('🔍 Running tests...')
        subprocess.run(['pytest', 'tests/'], check=False)

    def monitor(self) -> None:
        """Run all checks."""
        self.check_project_structure()
        self.lint_code()
        self.check_dependencies()
        self.check_system_health()
        self.run_tests()
