import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository
from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder


class BotConfig(TechConfigRepository):
    _instance: Optional['BotConfig'] = None

    def __new__(cls, env_path: Optional[Path] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, path_finder: ProjectPathFinder):
        if not self._initialized:
            self.env_path = path_finder.env_path
            load_dotenv(dotenv_path=self.env_path)
            self._initialized = True

            self.__bot_token = os.getenv("BOT_KEY")

    def get_bot_token(self) -> str:
        return self.__bot_token