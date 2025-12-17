from Scripts.Application.Interfaces.AdminHaircutRepository import AdminHaircutRepository
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class HaircutRequests(AdminHaircutRepository):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def add_haircut(self, username: str,
                    count_haircuts: int,
                    count_free_haircuts: int) -> bool:
        self.db.cursor.execute(
            "SELECT user_id FROM accounts WHERE username = ?",
            (username,)
        )
        user = self.db.cursor.fetchone()

        if user:
            print(count_haircuts)
            self.db.cursor.execute(
                "UPDATE accounts SET countHaircuts = ?, countFreeHaircuts = ? WHERE user_id = ?",
                (count_haircuts, count_free_haircuts, user[0])
            )
            self.db.connect.commit()
            return True

        return False