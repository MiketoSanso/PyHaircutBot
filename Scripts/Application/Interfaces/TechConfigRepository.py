from abc import ABC, abstractmethod


class TechConfigRepository(ABC):
    @abstractmethod
    def get_bot_token(self) -> str:
        pass