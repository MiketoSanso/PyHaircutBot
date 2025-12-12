from Scripts.Application.Interfaces.InfoRepository import InfoRepository


class GetPriceUseCase:
    def __init__(self,
                 info_repo: InfoRepository):
        self.info_repo = info_repo

    def execute(self) -> str:
        return self.info_repo.get_price()