from Scripts.Application.Interfaces.InfoRepository import InfoRepository
from Scripts.Infrastructure.Services.JsonConfigManager import JsonConfigManager


class GetPriceUseCase:
    def __init__(self,
                 info_repo: InfoRepository,
                 config_creator: JsonConfigManager):
        self.info_repo = info_repo
        self.config_creator = config_creator

    def execute(self) -> str:
        return self.info_repo.get_price()