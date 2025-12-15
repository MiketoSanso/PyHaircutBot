from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class ChangeCoinsForRefUseCase:
    def __init__(self, haircut_config_repo: HaircutConfigRepository):
        self.haircut_config_repo = haircut_config_repo

    def execute(self, coins_for_ref: int)-> bool:
        return self.haircut_config_repo.change_coins_for_ref(coins_for_ref)
