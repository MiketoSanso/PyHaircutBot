from Scripts.Application.Interfaces.AccountRepository import AccountRepository
from Scripts.Infrastructure.Services.JsonConfigManager import JsonConfigManager


class AddUserUseCase:
    def __init__(self,
                 account_repo: AccountRepository,
                 config_creator: JsonConfigManager):
        self.account_repo = account_repo
        self.config_creator = config_creator

    def execute(self, user_id: int, referrer_username: str):
        self.account_repo.add_referrer(user_id, referrer_username)