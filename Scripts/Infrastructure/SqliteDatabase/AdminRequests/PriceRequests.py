from Scripts.Application.Interfaces.PriceRepository import PriceRepository
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class PriceRequests(PriceRepository):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def add_service_price(self, name_service: str, cost_service: int):
        self.db.cursor.execute(
            'INSERT INTO price (nameService, costService) VALUES (?, ?)',
            (name_service, cost_service)
        )

    def get_count_services(self) -> int:
        self.db.cursor.execute('SELECT COUNT(*) FROM price')
        return self.db.cursor.fetchone()[0]

    def change_service_by_index(self) -> bool:
        pass

    def delete_service_by_index(self, row_index: int) -> bool:
        self.db.cursor.execute(
            'SELECT id FROM price ORDER BY id LIMIT 1 OFFSET ?',
            (row_index,)
        )
        result = self.db.cursor.fetchone()

        if result:
            service_id = result[0]
            self.db.cursor.execute(
                'DELETE FROM price WHERE id = ?',
            (service_id,)
            )
            self.db.conn.commit()
            return True
        return False