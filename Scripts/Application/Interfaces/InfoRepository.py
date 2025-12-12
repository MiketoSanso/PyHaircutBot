from abc import ABC, abstractmethod
from typing import Optional, Tuple


class InfoRepository(ABC):
    @abstractmethod
    def get_price(self) -> str:
        pass