from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ProjectDirectories:
    def __init__(self, base_dir: Path) -> None:
        self.PROJECT_DIR = base_dir / 'sanruum'
        self.LOG_DIR = base_dir / 'logs'
        self.DATA_DIR = base_dir / 'data'
        self.NLP_DATA_DIR = base_dir / 'data/nlp_data'
        self.MODEL_DIR = base_dir / 'models'
        self.MEMORY_DIR = base_dir / 'data/memory'
        self.USER_MEMORY_DIR = base_dir / 'data/memory/user_memory'
        self.INTENTS_DIR = base_dir / 'data/intents'
        self.RAW_DATA_DIR = base_dir / 'data/raw_data'
        self.PROCESSED_DATA_DIR = base_dir / 'data/processed_data'

    def init_dirs(self) -> None:
        for name, directory in self.__dict__.items():
            if isinstance(directory, Path) and not directory.exists():
                directory.mkdir(parents=True)
                logger.info(f'Creating directory: {name} -> {directory}')

    def list_dirs(self) -> dict[str, Path]:
        return {
            name: path for name, path in self.__dict__.items() if isinstance(path, Path)
        }


class ProjectFiles:
    @staticmethod
    def create_file(file_path: Path) -> str | None:
        if file_path.exists():
            return file_path.read_text()
        logger.warning(f'File not found: {file_path}')
        return None

    @staticmethod
    def read_file(file_path: Path) -> str | None:
        if file_path.exists():
            return file_path.read_text()
        logger.warning(f'File not found: {file_path}')
        return None

    @staticmethod
    def write_file(file_path: Path, content: str) -> None:
        file_path.write_text(content)
        logger.info(f'Updated file: {file_path}')

    @staticmethod
    def delete_file(file_path: Path) -> None:
        if file_path.exists():
            file_path.unlink()
            logger.info(f'Deleted file: {file_path}')


class ProjectManager:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    directories = ProjectDirectories(BASE_DIR)
    files = ProjectFiles()

    @classmethod
    def init_project(cls) -> None:
        cls.directories.init_dirs()

    @classmethod
    def self_repair(cls) -> None:
        logger.info('Sanruum AI Self-Repair System 🔄')
        cls.init_project()
        for name, path in cls.directories.list_dirs().items():
            if not path.exists():
                path.mkdir(parents=True)
                logger.warning(
                    f'[REPAIR] Missing directory recreated: {name} -> {path}',
                )
        logger.info('✅ All missing directories recreated')
