import sqlite3
from Scripts.Application.Interfaces.AccountRepository import AccountRepository
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class AccountRequests(AccountRepository):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def get_count_haircuts(self, user_id: int) -> int:
        try:
            self.db.cursor.execute(
                "SELECT countHaircuts FROM accounts WHERE user_id = ?",
                (user_id,)
            )
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def get_count_free_haircuts(self, user_id: int) -> int:
        try:
            self.db.cursor.execute(
                "SELECT countFreeHaircuts FROM accounts WHERE user_id = ?",
                (user_id,)
            )
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def get_referral_coins(self, user_id: int) -> int:
        try:
            self.db.cursor.execute(
                "SELECT referralCoins FROM accounts WHERE user_id = ?",
                (user_id,)
            )
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def get_user_id_by_username(self, username: str) -> int:
        try:
            self.db.cursor.execute(
                "SELECT user_id FROM accounts WHERE username = ?",
                (username,)
            )
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def add_user(self, user_id: int, username: str):
        self.db.cursor.execute("SELECT 1 FROM accounts WHERE user_id = ?", (user_id,))
        if self.db.cursor.fetchone():
            return False
        # Если нет - вставляем
        self.db.cursor.execute(
            'INSERT INTO accounts ('
            'user_id, '
            'username, '
            'referralCoins, '
            'countHaircuts, '
            'countFreeHaircuts, '
            'referrer, '
            'is_coins_added) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, username, 0, 0, 0, None, False)
        )

        self.db.connect.commit()

        if self.db.cursor.rowcount != 0:
            self.db.cache_users.add(user_id)

    def add_referrer(self, user_id: str, referrer_username: str) -> bool:
        if referrer_username.startswith('@'):
            referrer_username = referrer_username[1:]

        self.db.cursor.execute(
            "SELECT user_id FROM accounts WHERE username = ?",
            (referrer_username,)
        )
        referrer = self.db.cursor.fetchone()

        if referrer is None or referrer[0] == user_id:
            return False

        self.db.cursor.execute(
            "SELECT referrer FROM accounts WHERE user_id = ?",
            (user_id,)
        )
        existing_referrer = self.db.cursor.fetchone()
        if existing_referrer and existing_referrer[0] is not None:
            return False

        self.db.cursor.execute(
            "UPDATE accounts SET referrer = ? WHERE user_id = ?",
            (referrer_username, user_id)
        )

        self.db.connect.commit()
        return True
