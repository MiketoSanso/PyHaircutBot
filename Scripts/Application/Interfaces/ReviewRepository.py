from abc import ABC, abstractmethod
from typing import Optional, Tuple


class ReviewRepository(ABC):
    @abstractmethod
    def get_by_index(self, index: int) -> Optional[Tuple[str, str, int]]:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass

    @abstractmethod
    def upsert(self, user_id: int, username: str, text: str, rating: int) -> bool:
        pass