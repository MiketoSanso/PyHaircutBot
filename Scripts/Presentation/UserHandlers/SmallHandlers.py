import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters
from Scripts.Infrastructure.Database.UserRequests.AccountRequests import BaseCommands
from Scripts.Infrastructure.Services.ConfigCreator import ConfigCreator


class SmallHandlers:

    def __init__(self, base_commands_db: BaseCommands,
                 config_creator: ConfigCreator):
        self.config_creator = config_creator
        self.base_commands_db = base_commands_db

        self.reply_keyboard = ReplyKeyboardMarkup()
        self.setup_keyboards()

    def setup_handlers(self, application):
        application.add_handler(MessageHandler(filters.Regex(r'^👾'), self.start))
        application.add_handler(MessageHandler(filters.Regex(r'^💰'), self.price))
        application.add_handler(MessageHandler(filters.Regex(r'^👤'), self.account))
        application.add_handler(MessageHandler(filters.Regex(r'^❓'), self.help_command))

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("price", self.price))
        application.add_handler(CommandHandler("account", self.account))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(MessageHandler(filters.ALL, self.handle_message))

    def setup_keyboards(self):
        keyboard = [
            ["👾 Начать работу с ботом"],
            ["💰 Прайс"],
            ["👤 Аккаунт"],
            ["⭐ Посмотреть отзывы"],
            ["🏅 Оставить отзыв"],
            ["❓ Помощь"],
            ["👥 Реферальная система"],
            ["🤝 Добавить реферала"]
        ]

        self.reply_keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=False,
            one_time_keyboard=False
        )

    async def start(self, update: Update) -> None:
        await update.message.reply_text("\"Стриж и КО\"\n\n"
                                        "Привет! Рады видеть тебя здесь!\n"
                                        "Наша компания предоставляет услуги стрижки по очень выгодным ценам!\n"
                                        "Только у нас ты можешь пригласить друзей и получить бесплатные стрижки,\n"
                                        "Только у нас ты можешь попросить парикмахера выехать к тебе домой,\n"
                                        "А также именно у нас ты можешь получить бесплатные стрижки за частое посещение!\n\n"
                                        "Ждём тебя, наш парикмахер уже готовится!)",
                                        reply_markup=self.reply_keyboard
                                        )

    async def handle_message(self, update: Update) -> None:
        user = update.effective_user
        user_id = user.id
        username = user.username if user.username is not None else "user_" + user.id
        self.base_commands_db.add_user_to_db(user_id, username)

    async def price(self, update: Update) -> None:
        await update.message.reply_text("ПРАЙС\n\n"
                                        f"{self.base_commands_db.get_price()}\n")

    async def account(self, update: Update) -> None:
        user = update.effective_user
        user_id = user.id
        count = self.base_commands_db.get_count_haircuts(user_id) % self.config_creator.get_config_value(
            "count_haircuts_to_free") if self.base_commands_db.get_count_haircuts(user_id) != 0 else 3

        await update.message.reply_text(f"АККАУНТ\n\n"
                                        f"Количество стрижек у нас: {self.base_commands_db.get_count_haircuts(user_id)}\n"
                                        f"Количество бесплатных стрижек: {self.base_commands_db.get_count_free_haircuts(user_id)}\n\n"
                                        f"Реферальные баллы за приглашённых друзей: {self.base_commands_db.get_referral_coins(user_id)}\n"
                                        f"Оставшееся количество стрижек для получения 1 бесплатной: {count}\n")

    async def help_command(self, update: Update) -> None:
        await update.message.reply_text(f"СУЩЕСТВУЮЩИЕ КОМАНДЫ\n\n"
                                        f"/start - Узнать основную информацию.\n"
                                        f"/price - Узнать прайс на стрижки.\n"
                                        f"/account - Посмотреть свой баланс и статистику.\n"
                                        f"/referral - Информация о реферальной системе.\n"
                                        f"/reviews - Посмотреть отзывы\n"
                                        f"/addreview - Оставить отзыв\n"
                                        f"/help - Показать это сообщение\n"
                                        f"/specRef - Указать реферера (Человека, который привел вас сюда)")