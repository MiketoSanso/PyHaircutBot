import logging
import os
from pathlib import Path

class Logger:
    def __init__(self):
        self.setup_logging()
    def get_project_patch(self) -> Path:
        current = Path(__file__).resolve()

        for parent in [current] + list(current.parents):
            if (parent / ".git").exists():
                return parent

        return current

    def setup_logging(self):
        project_path = self.get_project_patch()

        os.makedirs(project_path, exist_ok=True)

        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(logging.INFO)

        self.app_handler = logging.FileHandler('app.log', encoding='utf-8')
        self.app_handler.setLevel(logging.INFO)
        self.app_handler.setFormatter(...)
        self.root_logger.addHandler(self.app_handler)

        self.error_handler = logging.FileHandler('errors.log', encoding='utf-8')
        self.error_handler.setLevel(logging.ERROR)
        self.error_handler.setFormatter(...)
        self.root_logger.addHandler(self.error_handler)