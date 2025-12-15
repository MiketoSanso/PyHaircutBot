from abc import ABC, abstractmethod


class TechConfigRepository(ABC):
    @abstractmethod
    def get_bot_token(self) -> str:
        pass

    @abstractmethod
    def get_admin_password(self) -> str:
        pass

    @abstractmethod
    def change_password(self, new_password: str) -> bool:
        pass