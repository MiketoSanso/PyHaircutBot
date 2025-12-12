from abc import ABC, abstractmethod
from typing import Any

from Scripts.Domain.HaircutConfig import HaircutConfig


class TechConfigRepository(ABC):
    @abstractmethod
    def get_bot_token(self) -> str:
        pass