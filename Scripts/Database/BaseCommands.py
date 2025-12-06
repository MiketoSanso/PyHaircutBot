import sqlite3

from Scripts.Database.HaircutDatabase import HaircutDatabase

class BaseCommands:
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def return_price(self) -> str:
        try:
            self.db.cursor.execute("SELECT nameService, costService FROM price")
            all_services = self.db.cursor.fetchall()

            services_list = []
            for nameService, costService in all_services:
                services_list.append(f"{nameService}: {costService} руб.\n")

            return "\n".join(services_list)
        except sqlite3.Error as e:
            return ""

    def return_count_haircuts(self, id_user: int) -> int:
        try:
            self.db.cursor.execute("SELECT countHaircuts FROM accounts WHERE idUser = ?", (id_user,))
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def return_count_free_haircuts(self, id_user: int) -> int:
        try:
            self.db.cursor.execute("SELECT countFreeHaircuts FROM accounts WHERE idUser = ?", (id_user,))
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def return_referal_coins(self, id_user: int) -> int:
        try:
            self.db.cursor.execute("SELECT referralCoins FROM accounts WHERE idUser = ?", (id_user,))
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def return_count_reviews(self) -> int:
        try:
            self.db.cursor.execute("SELECT COUNT(*) FROM reviews")
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def add_user_to_db(self,
                       id_user: str):
        self.db.cursor.execute('INSERT OR IGNORE INTO accounts (idUser, referralCoins, countHaircuts, countFreeHaircuts) VALUES (?, ?, ?, ?)',
                            (id_user, 0, 0, 0))

        self.db.connect.commit()

        if self.db.cursor.rowcount != 0:
            self.db.cache_users.add(id_user)

    def add_or_update_review(self, id_user: str, username: str, text_review: str, estimation: int) -> bool:

        self.db.cursor.execute('SELECT 1 FROM reviews WHERE idUser = ?', (id_user,))

        exists = self.db.cursor.fetchone() is not None
        status = True

        if exists:
            self.db.cursor.execute('UPDATE reviews SET idUser = ?, username = ?, textReview = ?, estimation = ?',
                                   (id_user, username, text_review, estimation))
            status = False
        else:
            self.db.cursor.execute('INSERT INTO reviews (idUser, username, textReview, estimation) VALUES (?, ?, ?, ?)',
                                (id_user, username, text_review, estimation))

        self.db.connect.commit()
        return status

    def get_review_by_index(self, index: int) -> tuple[str, str, int]:
        self.db.cursor.execute('SELECT username, textReview, estimation '
                               'FROM reviews '
                               'ORDER BY estimation DESC '
                               'LIMIT 1 OFFSET ?', (index,))

        return self.db.cursor.fetchone()