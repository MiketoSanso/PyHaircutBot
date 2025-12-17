from Scripts.Application.Interfaces.AccountRepository import AccountRepository
from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository


class GetUserHaircutsToFreeUseCase:
    def __init__(self,
                 account_repo: AccountRepository,
                 haircut_config_repo: HaircutConfigRepository):
        self.account_repo = account_repo
        self.haircut_config_repo = haircut_config_repo

    def execute(self, user_id: int) -> int:
        return ((self.haircut_config_repo.get_config_value("count_haircuts_to_free")
                 - self.account_repo.get_count_haircuts(user_id))
                % self.haircut_config_repo.get_config_value("count_haircuts_to_free"))



