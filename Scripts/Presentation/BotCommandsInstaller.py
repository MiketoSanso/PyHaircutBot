from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from Scripts.Presentation.UserHandlers.RefSystemHandlers import RefSystemHandlers
from Scripts.Presentation.UserHandlers.ReviewHandler import ReviewHandlers
from Scripts.Presentation.UserHandlers.SmallHandlers import SmallHandlers


class BotCommandsInstaller:

    def __init__(self,
                 small_handlers: SmallHandlers,
                 review_handlers: ReviewHandlers,
                 ref_system_handlers: RefSystemHandlers):
        self.small_handlers = small_handlers
        self.review_handlers = review_handlers
        self.ref_system_handlers = ref_system_handlers

        self.REFERRER_TEXT = 0

    def run(self):
        application = Application.builder().token(self.config.bot_token).build()
        self.setup_handlers(application)
        self.setup_keyboards()
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

    def setup_handlers(self, application):
        application.add_handler(MessageHandler(filters.Regex(r'^👾'), self.small_handlers.start))
        application.add_handler(MessageHandler(filters.Regex(r'^💰'), self.small_handlers.price))
        application.add_handler(MessageHandler(filters.Regex(r'^👤'), self.small_handlers.account))
        application.add_handler(MessageHandler(filters.Regex(r'^❓'), self.small_handlers.help_command))

        application.add_handler(CommandHandler("start", self.small_handlers.start))
        application.add_handler(CommandHandler("price", self.small_handlers.price))
        application.add_handler(CommandHandler("account", self.small_handlers.account))
        application.add_handler(CommandHandler("help", self.small_handlers.help_command))
        application.add_handler(MessageHandler(filters.ALL, self.small_handlers.handle_message))

    def setup_keyboards(self):
        pass