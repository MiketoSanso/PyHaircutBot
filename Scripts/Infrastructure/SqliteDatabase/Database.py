import sqlite3
from typing import Set


class HaircutDatabase:
    def __init__(self):
        self.cache_users: Set[int] = set()

        self.connect = sqlite3.connect('Barbershop.db')
        self.cursor = self.connect.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                user_id INT,
                username TEXT,
                textReview TEXT,
                estimation INT
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                user_id INT,
                username TEXT,
                referralCoins INT,
                countHaircuts INT,
                countFreeHaircuts INT,
                referrer TEXT,
                is_coins_added BOOL
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS price (
                nameService TEXT,
                costService INT
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INT
            )
            ''')

        self.cursor.execute('SELECT nameService FROM price')
        price = self.cursor.fetchone()
        if price is None:
            self.cursor.execute('INSERT INTO price (nameService, costService) VALUES (?, ?)',
                ("Стрижка", 500)
            )

            self.cursor.execute('INSERT INTO price (nameService, costService) VALUES (?, ?)',
                ("Бритьё бороды", 250)
            )
        self.load_known_users()

    def load_known_users(self):
        self.cursor.execute('SELECT user_id FROM accounts')
        self.cache_users.update([row[0] for row in self.cursor.fetchall()])
