from Scripts.Database.AdminCommands import AdminCommands
from Scripts.Database.BaseCommands import BaseCommands
from Scripts.Database.HaircutDatabase import HaircutDatabase
from Scripts.Bot import Bot

class DiContainer:

    def __init__(self):
        self.db = HaircutDatabase()
        self.base_commands = BaseCommands(self.db)
        self.admin_commands = AdminCommands(self.db)
        self.bot = Bot(self.base_commands, self.admin_commands)

        self.bot.run()

if __name__ == "__main__":
    container = DiContainer()