from Scripts.Application.Interfaces.AdminRepository import AdminRepository


class SearchAdminUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self, user_id: int) -> bool:
        return self.admin_repo.search_admin(user_id) is not None