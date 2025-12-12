from Scripts.Application.User.AddReferrerUseCase import AddReferrerUseCase
from Scripts.Application.User.AddUserUseCase import AddUserUseCase
from Scripts.Application.User.GetCountReviewsUseCase import GetCountReviewsUseCase
from Scripts.Application.User.GetPriceUseCase import GetPriceUseCase
from Scripts.Application.User.GetReviewByIndexUseCase import GetReviewByIndexUseCase
from Scripts.Application.User.GetTechDataUseCase import GetTechDataUseCase
from Scripts.Application.User.GetUserDataUseCase import GetUserDataUseCase
from Scripts.Application.User.UpsertReviewUseCase import UpsertReviewUseCase
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase
from Scripts.Infrastructure.SqliteDatabase.UserRequests.AccountRequests import AccountRequests
from Scripts.Infrastructure.SqliteDatabase.UserRequests.InfoRequests import InfoRequests
from Scripts.Infrastructure.SqliteDatabase.UserRequests.ReviewRequests import ReviewRequests
from Scripts.Presentation.BotCommandsInstaller import BotCommandsInstaller
from Scripts.Infrastructure.Services.JsonConfigManager import JsonConfigManager
from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder
from Scripts.Presentation.UserHandlers.RefSystemHandlers import RefSystemHandlers
from Scripts.Presentation.UserHandlers.ReviewHandler import ReviewHandlers
from Scripts.Presentation.UserHandlers.SmallHandlers import SmallHandlers


class Dependencies:

    def __init__(self):
        self.__path_finder = ProjectPathFinder()
        self.__db = HaircutDatabase()
        self.__set_infrastructure_commands()
        self.__set_use_cases()
        self.__set_handlers()

        self.__bot.run()

    def __set_infrastructure_commands(self):
        self.__account_repository = AccountRequests(self.__db)
        self.__info_repository = InfoRequests(self.__db)
        self.__review_repository = ReviewRequests(self.__db)
        self.__tech_config_repository = JsonConfigManager(self.__path_finder)

        #self.__admin_commands = AdminCommands(self.__db)

    def __set_use_cases(self):
        self.__add_referrer_uc = AddReferrerUseCase(self.__account_repository)
        self.__add_user_uc = AddUserUseCase(self.__account_repository)
        self.__get_count_reviews_uc = GetCountReviewsUseCase(self.__review_repository)
        self.__get_price_uc = GetPriceUseCase(self.__info_repository)
        self.__get_review_by_index_uc = GetReviewByIndexUseCase(self.__review_repository)
        self.__get_tech_data_uc = GetTechDataUseCase(self.__tech_config_repository)
        self.__get_user_data_uc = GetUserDataUseCase(self.__account_repository,
                                                     self.__tech_config_repository)
        self.__upsert_review_uc = UpsertReviewUseCase(self.__review_repository)

    def __set_handlers(self):
        ref_system_handlers = RefSystemHandlers(self.__get_tech_data_uc,
                                                self.__add_referrer_uc)
        review_handlers = ReviewHandlers(self.__upsert_review_uc,
                                         self.__get_review_by_index_uc,
                                         self.__get_count_reviews_uc)
        small_handlers = SmallHandlers(self.__get_user_data_uc,
                                       self.__add_user_uc,
                                       self.__get_price_uc)

        self.__bot = BotCommandsInstaller(small_handlers,
                                        review_handlers,
                                        ref_system_handlers)
