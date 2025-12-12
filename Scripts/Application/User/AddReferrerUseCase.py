from Scripts.Application.Interfaces.AccountRepository import AccountRepository


class AddReferrerUseCase:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def execute(self, user_id: int, username: str):
        self.account_repo.add_referrer(user_id, username)