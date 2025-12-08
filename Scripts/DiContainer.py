from Scripts.Database.AdminCommands import AdminCommands
from Scripts.Database.BaseCommands import BaseCommands
from Scripts.Database.HaircutDatabase import HaircutDatabase
from Scripts.Bot import Bot
from Scripts.Utils.ConfigCreator import ConfigCreator
from Scripts.Utils.ProjectPathFinder import ProjectPathFinder

class DiContainer:

    def __init__(self):
        self.path_finder = ProjectPathFinder()
        self.config_creator = ConfigCreator(self.path_finder)
        self.db = HaircutDatabase()
        self.base_commands = BaseCommands(self.db)
        self.admin_commands = AdminCommands(self.db)
        self.bot = Bot(self.base_commands, self.admin_commands, self.config_creator, self.path_finder)

        self.bot.run()