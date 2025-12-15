from Scripts.Application.Interfaces.AdminRepository import AdminRepository
from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository


class ChangeAdminPasswordUseCase:
    def __init__(self, admin_repo: AdminRepository,
                 tech_config_repo: TechConfigRepository):
        self.admin_repo = admin_repo
        self.tech_config_repo = tech_config_repo

    def execute(self, user_id, new_password: str)-> bool:
        if self.admin_repo.search_admin(user_id) is not None:
            return self.tech_config_repo.change_password(new_password)

        return False
