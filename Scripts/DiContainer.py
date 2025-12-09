from Scripts.Database.AdminRequests.AdminCommands import AdminCommands
from Scripts.Database.UserRequests.AccountRequests import AccountRequests
from Scripts.Database.UserRequests.InfoRequests import InfoCommands
from Scripts.Database.UserRequests.ReviewRequests import ReviewCommands
from Scripts.Database.HaircutDatabase import HaircutDatabase
from Scripts.Bot.BotCommandsInstaller import BotCommandsInstaller
from Scripts.Utils.ConfigCreator import ConfigCreator
from Scripts.Utils.ProjectPathFinder import ProjectPathFinder


class DiContainer:

    def __init__(self):
        self.__path_finder = ProjectPathFinder()
        self.__config_creator = ConfigCreator(self.__path_finder)
        self.__db = HaircutDatabase()
        self.__set_commands()
        self.bot = BotCommandsInstaller(self.__base_commands,
                                        self.__admin_commands,
                                        self.__config_creator,
                                        self.__path_finder)

        self.bot.run()

    def set_commands(self):
        self.__account_commands = AccountRequests(self.__db)
        self.__info_commands = InfoCommands(self.__db)
        self.__review_commands = ReviewCommands(self.__db)

        self.__admin_commands = AdminCommands(self.__db)
