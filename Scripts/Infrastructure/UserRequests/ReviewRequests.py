import sqlite3
from Scripts.Infrastructure.HaircutDatabase import HaircutDatabase


class ReviewRequests:
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def get_count_reviews(self) -> int:
        try:
            self.db.cursor.execute("SELECT COUNT(*) FROM reviews")
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def get_review_by_index(self, index: int) -> tuple[str, str, int]:
        self.db.cursor.execute('SELECT username, textReview, estimation '
                               'FROM reviews '
                               'ORDER BY estimation DESC '
                               'LIMIT 1 OFFSET ?', (index,))

        return self.db.cursor.fetchone()

    def add_or_update_review(self, id_user: str, username: str, text_review: str, estimation: int) -> bool:

        self.db.cursor.execute('SELECT 1 FROM reviews WHERE idUser = ?', (id_user,))

        exists = self.db.cursor.fetchone() is not None

        if exists:
            self.db.cursor.execute('UPDATE reviews SET idUser = ?, username = ?, textReview = ?, estimation = ?',
                                   (id_user, username, text_review, estimation))
        else:
            self.db.cursor.execute('INSERT INTO reviews (idUser, username, textReview, estimation) VALUES (?, ?, ?, ?)',
                                   (id_user, username, text_review, estimation))

        self.db.connect.commit()
        return not exists
