from Scripts.Application.Admin.AddAdminByIdUseCase import AddAdminByIdUseCase
from Scripts.Application.Admin.AddAdminByPasswordUseCase import AddAdminByPasswordUseCase
from Scripts.Application.Admin.AddHaircutByUsernameUseCase import AddHaircutByUsernameUseCase
from Scripts.Application.Admin.AddPointPriceUseCase import AddPointPriceUseCase
from Scripts.Application.Admin.ChangeAdminPasswordUseCase import ChangeAdminPasswordUseCase
from Scripts.Application.Admin.ChangeCoinsForFreeHaircutUseCase import ChangeCoinsForFreeHaircutUseCase
from Scripts.Application.Admin.ChangeCoinsForRefUseCase import ChangeCoinsForRefUseCase
from Scripts.Application.Admin.ChangeHaircutsToFreeUseCase import ChangeHaircutsToFreeUseCase
from Scripts.Application.Admin.ChangeRefHaircutsToBonusUseCase import ChangeRefHaircutsToBonusUseCase
from Scripts.Application.Admin.GetQrUseCase import GetQrUseCase
from Scripts.Application.Admin.GetReferencesUseCase import GetReferencesUseCase
from Scripts.Application.Admin.GetStatusUserUseCase import GetStatusUserUseCase
from Scripts.Application.Admin.RemoveAdminUseCase import RemoveAdminUseCase
from Scripts.Application.Admin.SearchAdminUseCase import SearchAdminUseCase
from Scripts.Application.User.AddReferrerUseCase import AddReferrerUseCase
from Scripts.Application.User.AddUserUseCase import AddUserUseCase
from Scripts.Application.User.GetBotKeyUseCase import GetBotKeyUseCase
from Scripts.Application.User.GetCountReviewsUseCase import GetCountReviewsUseCase
from Scripts.Application.User.GetPriceUseCase import GetPriceUseCase
from Scripts.Application.User.GetReviewByIndexUseCase import GetReviewByIndexUseCase
from Scripts.Application.User.GetHaircutDataUseCase import GetHaircutDataUseCase
from Scripts.Application.User.UpsertReviewUseCase import UpsertReviewUseCase
from Scripts.Application.User.UserData.GetUserFreeHaircutsUseCase import GetUserFreeHaircutsUseCase
from Scripts.Application.User.UserData.GetUserHaircutsToFreeUseCase import GetUserHaircutsToFreeUseCase
from Scripts.Application.User.UserData.GetUserHaircutsUseCase import GetUserHaircutsUseCase
from Scripts.Application.User.UserData.GetUserReferralCoinsUseCase import GetUserReferralCoinsUseCase
from Scripts.Infrastructure.Configs.BotConfig import BotConfig
from Scripts.Infrastructure.Services.PhotoFolderLoader import PhotoFolderLoader
from Scripts.Infrastructure.SqliteDatabase.AdminRequests.AdminRequests import AdminRequests
from Scripts.Infrastructure.SqliteDatabase.AdminRequests.HaircutRequests import HaircutRequests
from Scripts.Infrastructure.SqliteDatabase.AdminRequests.PriceRequests import PriceRequests
from Scripts.Infrastructure.SqliteDatabase.Database import HaircutDatabase
from Scripts.Infrastructure.SqliteDatabase.UserRequests.AccountRequests import AccountRequests
from Scripts.Infrastructure.SqliteDatabase.UserRequests.InfoRequests import InfoRequests
from Scripts.Infrastructure.SqliteDatabase.UserRequests.ReviewRequests import ReviewRequests
from Scripts.Presentation.AdminHandlers.AdminSmallHandlers import AdminSmallHandlers
from Scripts.Presentation.AdminHandlers.AdminStateHandlers import AdminStateHandlers
from Scripts.Presentation.AdminHandlers.ChangeHaircutConfigHandlers import ChangeHaircutConfigHandlers
from Scripts.Presentation.AdminHandlers.PriceHandlers import PriceHandlers
from Scripts.Presentation.BotCommandsInstaller import BotCommandsInstaller
from Scripts.Infrastructure.Services.JsonConfigManager import JsonConfigManager
from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder
from Scripts.Presentation.UserHandlers.RefSystemHandlers import RefSystemHandlers
from Scripts.Presentation.UserHandlers.ReviewHandler import ReviewHandlers
from Scripts.Presentation.UserHandlers.UserSmallHandlers import UserSmallHandlers


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
        self.__haircut_config_repository = JsonConfigManager(self.__path_finder)
        self.__tech_config_repository = BotConfig(self.__path_finder)

        self.__admin_repository = AdminRequests(self.__db)
        self.__admin_haircuts_repository = HaircutRequests(self.__db)
        self.__price_requests_repository = PriceRequests(self.__db)

        self.__photo_service = PhotoFolderLoader()

    def __set_use_cases(self):
        self.__add_admin_by_id_uc = AddAdminByIdUseCase(self.__admin_repository)
        self.__add_admin_by_password_uc = AddAdminByPasswordUseCase(self.__admin_repository,
                                                                    self.__tech_config_repository)
        self.__add_point_price_uc = AddPointPriceUseCase(self.__haircut_config_repository)
        self.__change_admin_password_uc = ChangeAdminPasswordUseCase(self.__admin_repository,
                                                                     self.__tech_config_repository)
        self.__change_coins_for_free_haircut_uc = ChangeCoinsForFreeHaircutUseCase(self.__haircut_config_repository)
        self.__change_coins_for_ref_uc = ChangeCoinsForRefUseCase(self.__haircut_config_repository)
        self.__change_haircuts_to_free_uc = ChangeHaircutsToFreeUseCase(self.__haircut_config_repository)
        self.__change_ref_haircuts_to_bonus_uc = ChangeRefHaircutsToBonusUseCase(self.__haircut_config_repository)
        self.__get_status_user_uc = GetStatusUserUseCase(self.__haircut_config_repository)
        self.__remove_admin_uc = RemoveAdminUseCase(self.__admin_repository)
        self.__search_admin_uc = SearchAdminUseCase(self.__admin_repository)
        self.__get_user_free_haircuts_uc = GetUserFreeHaircutsUseCase(self.__account_repository)
        self.__get_user_haircuts_uc = GetUserHaircutsUseCase(self.__account_repository)
        self.__get_user_referral_coins_uc = GetUserReferralCoinsUseCase(self.__account_repository)
        self.__get_user_haircuts_to_free_uc = GetUserHaircutsToFreeUseCase(self.__account_repository,
                                                                           self.__haircut_config_repository)
        self.__add_haircut_by_username_uc = AddHaircutByUsernameUseCase(self.__search_admin_uc,
                                                                        self.__get_user_haircuts_uc,
                                                                        self.__get_user_free_haircuts_uc,
                                                                        self.__haircut_config_repository,
                                                                        self.__admin_haircuts_repository,
                                                                        self.__account_repository)

        self.__add_referrer_uc = AddReferrerUseCase(self.__account_repository)
        self.__add_user_uc = AddUserUseCase(self.__account_repository)
        self.__get_count_reviews_uc = GetCountReviewsUseCase(self.__review_repository)
        self.__get_price_uc = GetPriceUseCase(self.__info_repository)
        self.__get_review_by_index_uc = GetReviewByIndexUseCase(self.__review_repository)
        self.__get_tech_data_uc = GetHaircutDataUseCase(self.__haircut_config_repository)
        self.__upsert_review_uc = UpsertReviewUseCase(self.__review_repository)
        self.__get_bot_key = GetBotKeyUseCase(self.__tech_config_repository)

        self.__get_qr_uc = GetQrUseCase(self.__photo_service, self.__path_finder)
        self.__get_references_uc = GetReferencesUseCase(self.__photo_service, self.__path_finder)

    def __set_handlers(self):
        admin_small_handlers = AdminSmallHandlers(self.__search_admin_uc,
                                                  self.__add_haircut_by_username_uc)
        admin_state_handlers = AdminStateHandlers(self.__add_admin_by_id_uc,
                                                  self.__add_admin_by_password_uc,
                                                  self.__remove_admin_uc,
                                                  self.__change_admin_password_uc)
        change_haircut_config_handlers = ChangeHaircutConfigHandlers(self.__change_coins_for_free_haircut_uc,
                                                                     self.__change_coins_for_ref_uc,
                                                                     self.__change_haircuts_to_free_uc,
                                                                     self.__change_ref_haircuts_to_bonus_uc)
        price_handlers = PriceHandlers()

        ref_system_handlers = RefSystemHandlers(self.__get_tech_data_uc,
                                                self.__add_referrer_uc)
        review_handlers = ReviewHandlers(self.__upsert_review_uc,
                                         self.__get_review_by_index_uc,
                                         self.__get_count_reviews_uc)
        small_handlers = UserSmallHandlers(self.__get_user_free_haircuts_uc,
                                           self.__get_user_haircuts_uc,
                                           self.__get_user_referral_coins_uc,
                                           self.__get_user_haircuts_to_free_uc,
                                           self.__add_user_uc,
                                           self.__get_price_uc,
                                           self.__get_qr_uc,
                                           self.__get_references_uc)

        self.__bot = BotCommandsInstaller(small_handlers,
                                          admin_small_handlers,
                                          admin_state_handlers,
                                          change_haircut_config_handlers,
                                          price_handlers,
                                          review_handlers,
                                          ref_system_handlers,
                                          self.__get_bot_key)
