import sqlite3
from Scripts.Application.Interfaces.InfoRepository import InfoRepository
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase


class InfoRequests(InfoRepository):
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def get_price(self) -> str:
        try:
            self.db.cursor.execute("SELECT nameService, costService FROM price")
            all_services = self.db.cursor.fetchall()

            services_list = []
            for nameService, costService in all_services:
                services_list.append(f"{nameService}: {costService} руб.\n")

            return "\n".join(services_list)
        except sqlite3.Error as e:
            return ""
