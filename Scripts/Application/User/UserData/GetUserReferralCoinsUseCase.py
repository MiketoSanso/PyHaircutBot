from Scripts.Application.Interfaces.AccountRepository import AccountRepository


class GetUserReferralCoinsUseCase:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def execute(self, user_id: int) -> int:
        return self.account_repo.get_referral_coins(user_id)

