from abc import ABC, abstractmethod
from typing import Optional, Tuple


class AccountRepository(ABC):
    @abstractmethod
    def get_count_haircuts(self, user_id: int) -> int:
        pass

    @abstractmethod
    def get_count_free_haircuts(self, user_id: int) -> int:
        pass

    @abstractmethod
    def get_referral_coins(self, user_id: int) -> int:
        pass

    @abstractmethod
    def add_user(self, user_id: int, username: str):
        pass

    @abstractmethod
    def add_referrer(self, user_id: int, referrer_username: str) -> bool:
        pass