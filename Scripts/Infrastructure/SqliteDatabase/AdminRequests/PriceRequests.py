from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class PriceRequests:
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def add_service_price(self, name_service: str, cost_service: int):
        self.db.cursor.execute(
            'INSERT INTO price (nameService, costService) VALUES (?, ?)',
            (name_service, cost_service)
        )

    def get_all_services(self):
        pass

    def change_service_by_index(self):
        pass

    def delete_service_by_index(self):
        pass