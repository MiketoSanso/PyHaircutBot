from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class ChangeCoinsForFreeHaircutUseCase:
    def __init__(self, haircut_config_repo: HaircutConfigRepository):
        self.haircut_config_repo = haircut_config_repo

    def execute(self, haircut_for_free_haircut: int):
        self.haircut_config_repo.change_coins_for_free_haircut(haircut_for_free_haircut)
