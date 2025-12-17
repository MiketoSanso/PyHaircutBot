from Scripts.Application.Interfaces.AdminRepository import AdminRepository
from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository


class AddAdminByPasswordUseCase:
    def __init__(self, admin_repo: AdminRepository,
                 tech_config_repo: TechConfigRepository):
        self.admin_repo = admin_repo
        self.tech_config_repo = tech_config_repo

    def execute(self, user_id: int, password: str)-> bool:
        if password == self.tech_config_repo.get_admin_password():
            return self.admin_repo.add_admin(user_id)

        return False
