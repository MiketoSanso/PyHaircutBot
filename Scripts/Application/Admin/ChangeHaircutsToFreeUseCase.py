from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class ChangeHaircutsToFreeUseCase:
    def __init__(self, haircut_config_repo: HaircutConfigRepository):
        self.haircut_config_repo = haircut_config_repo

    def execute(self, count_haircuts_to_free: int)-> bool:
        return self.haircut_config_repo.change_haircuts_to_free(count_haircuts_to_free)
