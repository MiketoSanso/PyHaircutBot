from Scripts.Application.Interfaces.AccountRepository import AccountRepository
from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class GetUserDataUseCase:
    def __init__(self,
                 account_repo: AccountRepository,
                 haircut_config_repo: HaircutConfigRepository):
        self.account_repo = account_repo
        self.haircut_config_repo = haircut_config_repo

    def execute(self, user_id: int) -> dict:
        haircuts = self.account_repo.get_count_haircuts(user_id)
        free_haircuts = self.account_repo.get_count_free_haircuts(user_id)
        referral_coins = self.account_repo.get_referral_coins(user_id)
        haircuts_to_free = self.account_repo.get_count_haircuts(user_id) % self.haircut_config_repo.get_config_value(
            "count_haircuts_to_free") if self.account_repo.get_count_haircuts(user_id) != 0 else 3

        return {
            "haircuts": haircuts,
            "free_haircuts": free_haircuts,
            "referral_coins": referral_coins,
            "haircuts_to_free": haircuts_to_free
        }

