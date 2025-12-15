from Scripts.Application.Interfaces.AdminHaircutRepository import AdminHaircutRequests
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class HaircutRequests(AdminHaircutRequests):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def add_haircut(self, username: str) -> bool:
        self.db.cursor.execute(
            "SELECT user_id FROM accounts WHERE username = ?",
            (username,)
        )
        referrer = self.db.cursor.fetchone()

        if referrer:
            pass

        return False