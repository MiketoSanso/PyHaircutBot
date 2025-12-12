import sqlite3
from Scripts.Application.Interfaces.AccountRepository import AccountRepository
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class AccountRequests(AccountRepository):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def get_count_haircuts(self, id_user: int) -> int:
        try:
            self.db.cursor.execute("SELECT countHaircuts FROM accounts WHERE idUser = ?", (id_user,))
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def get_count_free_haircuts(self, id_user: int) -> int:
        try:
            self.db.cursor.execute("SELECT countFreeHaircuts FROM accounts WHERE idUser = ?", (id_user,))
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def get_referral_coins(self, id_user: int) -> int:
        try:
            self.db.cursor.execute("SELECT referralCoins FROM accounts WHERE idUser = ?", (id_user,))
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def add_user(self, id_user: int, username: str):
        self.db.cursor.execute(
            'INSERT OR IGNORE INTO accounts (idUser, username, referralCoins, countHaircuts, countFreeHaircuts) VALUES (?, ?, ?, ?, ?)',
            (id_user, username, 0, 0, 0))

        self.db.connect.commit()

        if self.db.cursor.rowcount != 0:
            self.db.cache_users.add(id_user)

    def add_referrer(self, id_user: str, referrer_username: str) -> bool:
        if referrer_username.startswith('@'):
            referrer_username = referrer_username[1:]

        self.db.cursor.execute(
            "SELECT idUser FROM accounts WHERE username = ?",
            (referrer_username,)
        )
        referrer_row = self.db.cursor.fetchone()

        if referrer_row is None:
            return False

        self.db.cursor.execute("UPDATE accounts SET idUser = ?, referrer = ?",
                               id_user, referrer_username)

        return True
