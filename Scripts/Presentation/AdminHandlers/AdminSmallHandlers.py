from Scripts.Infrastructure.Database.Database import HaircutDatabase

class AdminCommands:
    def __init__(self, db: HaircutDatabase):
        self.db = db

    def admin_help(self):
        pass