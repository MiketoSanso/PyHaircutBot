from Scripts.Application.Interfaces.AdminRepository import AdminRepository
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class AdminRequests(AdminRepository):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def search_admin(self, user_id) -> tuple[int,]:
        self.db.cursor.execute(
            "SELECT user_id FROM admins WHERE user_id = ?",
            (user_id,)
        )
        return self.db.cursor.fetchone()

    def add_admin(self, user_id: int)-> bool:
        user = self.search_admin(user_id)
        if user is not None:
            return False

        self.db.cursor.execute(
            "INSERT INTO admins (user_id) VALUES (?)",
            (user_id,)
        )
        self.db.connect.commit()

        return True

    def remove_admin(self, user_id)-> bool:
        user = self.search_admin(user_id)
        if user is None:
            return False

        self.db.cursor.execute(
            "DELETE FROM admins WHERE user_id = ?",
            (user_id,)
        )
        self.db.connect.commit()

        return True

    def add_haircut(self, user_id: str) -> bool:
        self.db.cursor.execute(
            "SELECT user_id FROM accounts WHERE user_id = ?",
            (referrer_username,)
        )
        referrer = self.db.cursor.fetchone()