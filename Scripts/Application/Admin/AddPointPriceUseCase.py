from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class AddPointPriceUseCase:
    def __init__(self, haircut_config_repo: HaircutConfigRepository):
        self.haircut_config_repo = haircut_config_repo

    def execute(self, haircut_for_free_haircut: int):
         pass