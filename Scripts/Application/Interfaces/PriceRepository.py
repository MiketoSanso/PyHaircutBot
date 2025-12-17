from abc import ABC, abstractmethod
from typing import Optional, Tuple


class PriceRepository(ABC):
    @abstractmethod
    def add_service_price(self, name_service: str, cost_service: int):
        pass

    @abstractmethod
    def get_all_services(self):
        pass

    @abstractmethod
    def change_service_by_index(self):
        pass

    @abstractmethod
    def delete_service_by_index(self):
        pass