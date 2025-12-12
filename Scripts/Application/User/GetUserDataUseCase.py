from Scripts.Application.Interfaces.AccountRepository import AccountRepository
from Scripts.Infrastructure.Services.JsonConfigManager import JsonConfigManager


class GetUserDataUseCase:
    def __init__(self,
                 account_repo: AccountRepository,
                 config_creator: JsonConfigManager):
        self.account_repo = account_repo
        self.config_creator = config_creator

    def execute(self, user_id: int) -> dict:
        haircuts = self.account_repo.get_count_haircuts(user_id)
        free_haircuts = self.account_repo.get_count_free_haircuts(user_id)
        referral_coins = self.account_repo.get_referral_coins(user_id)
        haircuts_to_free = self.account_repo.get_count_haircuts(user_id) % self.config_creator.get_config_value(
            "count_haircuts_to_free") if self.account_repo.get_count_haircuts(user_id) != 0 else 3

        return {
            "haircuts": haircuts,
            "free_haircuts": free_haircuts,
            "referral_coins": referral_coins,
            "haircuts_to_free": haircuts_to_free
        }

