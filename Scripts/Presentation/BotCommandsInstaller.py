from telegram import BotCommand
from telegram.ext import Application
from Scripts.Application.User.GetBotKeyUseCase import GetBotKeyUseCase
from Scripts.Presentation.UserHandlers.RefSystemHandlers import RefSystemHandlers
from Scripts.Presentation.UserHandlers.ReviewHandler import ReviewHandlers
from Scripts.Presentation.UserHandlers.UserSmallHandlers import UserSmallHandlers


class BotCommandsInstaller:

    def __init__(self,
                 small_handlers: UserSmallHandlers,
                 review_handlers: ReviewHandlers,
                 ref_system_handlers: RefSystemHandlers,
                 get_bot_key_uc: GetBotKeyUseCase):
        self.get_bot_key_uc = get_bot_key_uc
        self.small_handlers = small_handlers
        self.review_handlers = review_handlers
        self.ref_system_handlers = ref_system_handlers

        self.REFERRER_TEXT = 0

    def run(self):
        application = Application.builder().token(self.get_bot_key_uc.execute()).build()
        self.small_handlers.setup_handlers(application)
        self.review_handlers.setup_handlers(application)
        self.ref_system_handlers.setup_handlers(application)

        async def set_commands(app):
            commands = [
                BotCommand("start", "Начать работу"),
                BotCommand("price", "Прайс на услуги"),
                BotCommand("account", "Мой аккаунт"),
                BotCommand("referral", "Реферальная система"),
                BotCommand("reviews", "Посмотреть отзывы"),
                BotCommand("add_review", "Оставить отзыв"),
                BotCommand("help", "Помощь и команды"),
                BotCommand("spec_ref", "Добавить реферала")
            ]
            await app.bot.set_my_commands(commands)

        application.post_init = set_commands
        application.run_polling()