from Scripts.Application.Interfaces.AdminRepository import AdminRepository


class AddAdminByPasswordUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo
        pass


    def execute(self, user_id: int, password: str)-> bool:
        if True:
            return self.admin_repo.add_admin(user_id)

        return False
