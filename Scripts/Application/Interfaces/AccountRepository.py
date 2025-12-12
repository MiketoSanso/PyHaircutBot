from abc import ABC, abstractmethod
from typing import Optional, Tuple


class AccountRepository(ABC):
    @abstractmethod
    def get_count_haircuts(self, id_user: int) -> int:
        pass

    @abstractmethod
    def get_count_free_haircuts(self, id_user: int) -> int:
        pass

    @abstractmethod
    def get_referral_coins(self, id_user: int) -> int:
        pass

    @abstractmethod
    def add_user(self, id_user: int, username: str):
        pass

    @abstractmethod
    def add_referrer(self, id_user: int, referrer_username: str) -> bool:
        pass