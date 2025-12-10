from Scripts.Infrastructure.Database.Database import HaircutDatabase
from Scripts.Infrastructure.Database.UserRequests.AccountRequests import AccountRequests
from Scripts.Infrastructure.Services.ConfigCreator import ConfigCreator


class GetUserDataUseCase:
    def __init__(self,
                 db_commands: AccountRequests,
                 database: HaircutDatabase,
                 config_creator: ConfigCreator):
        self.db = db_commands
        self.database = database
        self.config_creator = config_creator

    def execute(self, id_user) -> dict:
        count_haircuts = self.db.get_count_haircuts(id_user)
        count_free_haircuts = self.db.get_count_free_haircuts(id_user)
        referral_coins = self.db.get_referral_coins(id_user)



