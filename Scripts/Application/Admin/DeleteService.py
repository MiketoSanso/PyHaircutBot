from typing import List
from Scripts.Application.Interfaces.PriceRepository import PriceRepository


class DeleteService:
    def __init__(self, price_repo: PriceRepository):
        self.price_repo = price_repo

    def execute(self, index) -> bool:
        return self.price_repo.delete_service_by_index(index)
