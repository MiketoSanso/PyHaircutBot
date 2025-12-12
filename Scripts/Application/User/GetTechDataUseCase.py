from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository


class GetTechDataUseCase:
    def __init__(self,
                 tech_config_repo: TechConfigRepository):
        self.tech_config_repo = tech_config_repo

    def execute(self) -> dict:
        ref_haircuts_to_bonus = self.tech_config_repo.get_config_value("count_referral_haircuts_to_bonus")
        coins_for_referral = self.tech_config_repo.get_config_value("coins_for_one_referral")
        coins_free_haircut = self.tech_config_repo.get_config_value("coins_for_free_haircut")

        return {
            "count_referral_haircuts_to_bonus": ref_haircuts_to_bonus,
            "coins_for_one_referral": coins_for_referral,
            "coins_for_free_haircut": coins_free_haircut
        }
