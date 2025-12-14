from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class ChangeRefHaircutsToBonusUseCase:
    def __init__(self, haircut_config_repo: HaircutConfigRepository):
        self.haircut_config_repo = haircut_config_repo

    def execute(self, ref_haircuts_to_bonus: int):
        self.haircut_config_repo.change_ref_haircuts_to_bonus(ref_haircuts_to_bonus)
