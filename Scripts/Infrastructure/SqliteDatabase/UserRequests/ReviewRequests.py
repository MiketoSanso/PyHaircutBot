import sqlite3
from Scripts.Application.Interfaces.ReviewRepository import ReviewRepository
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class ReviewRequests(ReviewRepository):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def get_count(self) -> int:
        try:
            self.db.cursor.execute("SELECT COUNT(*) FROM reviews")
            result = self.db.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            return 0

    def get_by_index(self, index: int) -> tuple[str, str, int]:
        self.db.cursor.execute(
            'SELECT username, textReview, estimation '
            'FROM reviews '
            'ORDER BY estimation DESC '
            'LIMIT 1 OFFSET ?',
            (index,)
        )

        return self.db.cursor.fetchone()

    def upsert(self, user_id: int, username: str, text_review: str, estimation: int) -> bool:

        self.db.cursor.execute(
            'SELECT 1 FROM reviews WHERE user_id = ?',
            (user_id,)
        )

        exists = self.db.cursor.fetchone() is not None

        if exists:
            self.db.cursor.execute(
                'UPDATE reviews SET user_id = ?, username = ?, textReview = ?, estimation = ?',
                (user_id, username, text_review, estimation)
            )
        else:
            self.db.cursor.execute(
                'INSERT INTO reviews (user_id, username, textReview, estimation) VALUES (?, ?, ?, ?)',
                (user_id, username, text_review, estimation)
            )

        self.db.connect.commit()
        return not exists
