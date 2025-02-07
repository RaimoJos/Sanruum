import os
import subprocess

from sanruum.utils.logger import logger


class SanruumMonitor:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def check_project_structure(self):
        """Ensure required directories and files exists."""
        required_dirs = [
            "sanruum",
            "sanruum/ai_core",
            "sanruum/utils",
            "tests",
        ]
        missing_dirs = [
            d
            for d in required_dirs
            if not os.path.exists(os.path.join(self.base_dir, d))
        ]

        if missing_dirs:
            logger.warning(
                f"🚨 Missing directories: {', '.join(missing_dirs)}"
            )
        else:
            logger.info("✅ Project structure looks good.")

    def lint_code(self):
        """Run code formatters and linters."""
        logger.info("🛠 Running code format checks...")
        subprocess.run(["poetry", "run", "black", self.base_dir], check=False)
        subprocess.run(["isort", self.base_dir], check=False)
        subprocess.run(["flake8", self.base_dir], check=False)

    @staticmethod
    def run_tests():
        """Run automated tests."""
        logger.info("🔍 Running tests...")
        subprocess.run(["pytest", "tests/"], check=False)

    def monitor(self):
        """Run all checks."""
        self.check_project_structure()
        self.lint_code()
        self.run_tests()
