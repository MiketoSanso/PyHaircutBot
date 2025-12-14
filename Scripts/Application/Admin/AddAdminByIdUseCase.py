from Scripts.Application.Interfaces.AdminRepository import AdminRepository


class AddAdminByIdUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self, user_id: int, new_admin_id: int)-> bool:
        if self.admin_repo.search_admin(user_id):
            return self.admin_repo.add_admin(new_admin_id)

        return False
