from abc import ABC, abstractmethod
from typing import Any

from Scripts.Domain.HaircutConfig import HaircutConfig


class TechConfigRepository(ABC):
    @abstractmethod
    def load_or_create_config(self):
        pass

    @abstractmethod
    def create_default_config(self):
        pass

    @abstractmethod
    def save_config(self):
        pass

    @abstractmethod
    def change_haircuts_to_free(self, count: int):
        pass

    @abstractmethod
    def get_config_value(self, key: str) -> Any:
        pass