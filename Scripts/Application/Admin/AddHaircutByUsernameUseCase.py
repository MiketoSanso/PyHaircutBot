from Scripts.Application.Admin.SearchAdminUseCase import SearchAdminUseCase
from Scripts.Application.Interfaces.AdminRepository import AdminRepository
from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository


class AddHaircutByUsernameUseCase:
    def __init__(self, search_admin_uc: SearchAdminUseCase):
        self.search_admin_uc = search_admin_uc

    def execute(self, user_id: int, username: str)-> bool:
        if self.search_admin_uc.execute(user_id):
            return self.admin_repo.add_admin(user_id)

        return False
 hjk