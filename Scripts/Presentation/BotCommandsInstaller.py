from telegram import BotCommand
from telegram.ext import Application
from Scripts.Application.User.GetBotKeyUseCase import GetBotKeyUseCase
from Scripts.Presentation.AdminHandlers.AdminSmallHandlers import AdminSmallHandlers
from Scripts.Presentation.AdminHandlers.AdminStateHandlers import AdminStateHandlers
from Scripts.Presentation.AdminHandlers.ChangeHaircutConfigHandlers import ChangeHaircutConfigHandlers
from Scripts.Presentation.AdminHandlers.PriceHandlers import PriceHandlers
from Scripts.Presentation.UserHandlers.RefSystemHandlers import RefSystemHandlers
from Scripts.Presentation.UserHandlers.ReviewHandler import ReviewHandlers
from Scripts.Presentation.UserHandlers.UserSmallHandlers import UserSmallHandlers


class BotCommandsInstaller:

    def __init__(self,
                 user_small_handlers: UserSmallHandlers,
                 admin_small_handlers: AdminSmallHandlers,
                 admin_state_handlers: AdminStateHandlers,
                 change_haircut_config_handlers: ChangeHaircutConfigHandlers,
                 price_handlers: PriceHandlers,
                 review_handlers: ReviewHandlers,
                 ref_system_handlers: RefSystemHandlers,
                 get_bot_key_uc: GetBotKeyUseCase):
        self.admin_small_handlers = admin_small_handlers
        self.admin_state_handlers = admin_state_handlers
        self.change_haircut_config_handlers = change_haircut_config_handlers
        self.price_handlers = price_handlers
        self.get_bot_key_uc = get_bot_key_uc
        self.user_small_handlers = user_small_handlers
        self.review_handlers = review_handlers
        self.ref_system_handlers = ref_system_handlers

        self.REFERRER_TEXT = 0

    def run(self):
        application = Application.builder().token(self.get_bot_key_uc.execute()).build()
        self.user_small_handlers.setup_handlers(application)
        self.review_handlers.setup_handlers(application)
        self.ref_system_handlers.setup_handlers(application)
        self.admin_small_handlers.setup_handlers(application)
        self.admin_state_handlers.setup_handlers(application)
        self.change_haircut_config_handlers.setup_handlers(application)
        self.price_handlers.setup_handlers(application)

        async def set_commands(app):
            commands = [
                BotCommand("start", "Начать работу"),
                BotCommand("price", "Прайс на услуги"),
                BotCommand("account", "Мой аккаунт"),
                BotCommand("referral", "Реферальная система"),
                BotCommand("reviews", "Посмотреть отзывы"),
                BotCommand("add_review", "Оставить отзыв"),
                BotCommand("references", "Примеры работ"),
                BotCommand("qr_pay", "QR-код оплаты"),
                BotCommand("help", "Помощь и команды"),
                BotCommand("spec_ref", "Добавить реферала")
            ]
            await app.bot.set_my_commands(commands)

        application.post_init = set_commands
        application.run_polling()