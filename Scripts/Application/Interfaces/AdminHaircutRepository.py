from abc import ABC, abstractmethod
from typing import Optional, Tuple


class AdminHaircutRepository(ABC):
    @abstractmethod
    def add_haircut(self, username: str,
                    count_haircuts: int,
                    count_free_haircuts: int) -> bool:
        pass