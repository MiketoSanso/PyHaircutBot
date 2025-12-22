from typing import List
from Scripts.Application.Interfaces.PriceRepository import PriceRepository


class GetCountServices:
    def __init__(self, price_repo: PriceRepository):
        self.price_repo = price_repo

    def execute(self) -> int:
        return self.price_repo.get_count_services()
