import sqlite3
from typing import Set

class HaircutDatabase:
    def __init__(self):
        self.cache_users: Set[int] = set()

        self.connect = sqlite3.connect('../../Barbershop.db')
        self.cursor = self.connect.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                idUser INT,
                username TEXT,
                textReview TEXT,
                estimation INT
                )
                ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                idUser INT,
                referralCoins INT,
                countHaircuts INT,
                countFreeHaircuts INT
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS price (
                nameService TEXT,
                costService INT
            )
            ''')

        self.LoadKnownUsers()

        self.cursor.execute("SELECT nameService FROM price")

        if self.cursor.fetchall() == []:
            self.cursor.execute('INSERT INTO price (nameService, costService) VALUES (?, ?)', ("Обычная стрижка", 500))
            self.cursor.execute('INSERT INTO price (nameService, costService) VALUES (?, ?)', ("Бритьё бороды", 250))
            self.cursor.execute('INSERT INTO price (nameService, costService) VALUES (?, ?)', ("Мытье головы", 150))
        self.connect.commit()

    def LoadKnownUsers(self):
        self.cursor.execute('SELECT idUser FROM accounts')
        self.cache_users.update([row[0] for row in self.cursor.fetchall()])

    def Close(self):
        if self.connect:
            self.connect.close()