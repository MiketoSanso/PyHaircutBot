from Scripts.Application.Interfaces.AdminRepository import AdminRepository


class RemoveAdminUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self, user_id: int, delete_admin_id: int) -> bool:
        if self.admin_repo.search_admin(user_id) and self.admin_repo.search_admin(delete_admin_id):
            return self.admin_repo.remove_admin(delete_admin_id)

        return False