from abc import ABC, abstractmethod
from typing import Optional, Tuple


class AdminRepository(ABC):
    @abstractmethod
    def search_admin(self, user_id) -> tuple[int,]:
        pass

    @abstractmethod
    def add_admin(self, user_id: int)-> bool:
        pass

    @abstractmethod
    def remove_admin(self, user_id)-> bool:
        pass