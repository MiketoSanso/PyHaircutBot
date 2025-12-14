from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class GetHaircutDataUseCase:
    def __init__(self,
                 haircut_config_repo: HaircutConfigRepository):
        self.haircut_config_repo = haircut_config_repo

    def execute(self) -> dict:
        ref_haircuts_to_bonus = self.haircut_config_repo.get_config_value("count_referral_haircuts_to_bonus")
        coins_for_referral = self.haircut_config_repo.get_config_value("coins_for_one_referral")
        coins_free_haircut = self.haircut_config_repo.get_config_value("coins_for_free_haircut")

        return {
            "count_referral_haircuts_to_bonus": ref_haircuts_to_bonus,
            "coins_for_one_referral": coins_for_referral,
            "coins_for_free_haircut": coins_free_haircut
        }
