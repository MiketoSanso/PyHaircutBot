from Scripts.Application.Admin.SearchAdminUseCase import SearchAdminUseCase
from Scripts.Application.Interfaces.AccountRepository import AccountRepository
from Scripts.Application.Interfaces.AdminHaircutRepository import AdminHaircutRepository
from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository
from Scripts.Application.User.UserData.GetUserFreeHaircutsUseCase import GetUserFreeHaircutsUseCase
from Scripts.Application.User.UserData.GetUserHaircutsUseCase import GetUserHaircutsUseCase


class AddHaircutByUsernameUseCase:
    def __init__(self, search_admin_uc: SearchAdminUseCase,
                 get_user_haircuts_uc: GetUserHaircutsUseCase,
                 get_user_haircuts_free_uc: GetUserFreeHaircutsUseCase,
                 haircut_config_repo: HaircutConfigRepository,
                 admin_haircut_repository: AdminHaircutRepository,
                 account_repo: AccountRepository):
        self.account_repo = account_repo
        self.get_user_haircuts_free_uc = get_user_haircuts_free_uc
        self.haircut_config_repo = haircut_config_repo
        self.get_user_haircuts_uc = get_user_haircuts_uc
        self.search_admin_uc = search_admin_uc
        self.admin_haircut_repository = admin_haircut_repository

    def execute(self, user_id: int, username: str)-> bool:
        if self.search_admin_uc.execute(user_id):
            id_by_username = self.account_repo.get_user_id_by_username(username)
            print(id_by_username)

            if id_by_username == 0:
                return False

            count_haircuts_to_free = self.haircut_config_repo.get_config_value("count_haircuts_to_free")
            count_haircuts = self.get_user_haircuts_uc.execute(id_by_username) + 1
            user_free_haircuts = self.get_user_haircuts_free_uc.execute(id_by_username)

            count_free_haircuts = user_free_haircuts + 1 \
                if count_haircuts % count_haircuts_to_free == 0 \
                else user_free_haircuts



            return self.admin_haircut_repository.add_haircut(username, count_haircuts, count_free_haircuts)

        return False