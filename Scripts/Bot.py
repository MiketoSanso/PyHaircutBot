import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from dotenv import load_dotenv
from Scripts.Database.BaseCommands import BaseCommands
from Scripts.Database.AdminCommands import AdminCommands
from Scripts.Utils.ConfigCreator import ConfigCreator
from Scripts.Utils.ProjectPathFinder import ProjectPathFinder

class Bot:

    def __init__(self, base_commands_db: BaseCommands,
                 admin_commands_db: AdminCommands,
                 config_creator: ConfigCreator,
                 path_finder: ProjectPathFinder):
        self.path_finder = path_finder
        self.config_creator = config_creator
        self.base_commands_db = base_commands_db
        self.admin_commands_db = admin_commands_db

        self.REVIEW_TEXT, self.REVIEW_RATING = range(2)

        env_path = self.path_finder.get_project_path() / "tech.env"
        load_dotenv(dotenv_path=env_path)

        self.BOT_TOKEN = os.getenv("BOT_KEY")

    def run(self):
        application = Application.builder().token(self.BOT_TOKEN).build()
        self.setup_handlers(application)
        self.setup_keyboards()

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
        review_conversation = ConversationHandler(
            entry_points=[
                CommandHandler("add_review", self.add_review),
                MessageHandler(filters.Regex(r'^🏅'), self.add_review)
            ],
            states={
                self.REVIEW_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.review_text_received)],
                self.REVIEW_RATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.review_rating_received)],
            },
            fallbacks=
            [
                CommandHandler("cancel", self.cancel),
                MessageHandler(filters.COMMAND, self.cancel)
            ],
        )

        application.add_handler(review_conversation)
        application.add_handler(CallbackQueryHandler(self.button_handler))

        application.add_handler(MessageHandler(filters.Regex(r'^👾'), self.start))
        application.add_handler(MessageHandler(filters.Regex(r'^💰'), self.price))
        application.add_handler(MessageHandler(filters.Regex(r'^👤'), self.account))
        application.add_handler(MessageHandler(filters.Regex(r'^⭐'), self.reviews))
        application.add_handler(MessageHandler(filters.Regex(r'^❓'), self.help_command))
        application.add_handler(MessageHandler(filters.Regex(r'^👥'), self.referral))
        application.add_handler(MessageHandler(filters.Regex(r'^🤝'), self.specify_refferal))

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("price", self.price))
        application.add_handler(CommandHandler("account", self.account))
        application.add_handler(CommandHandler("referral", self.referral))
        application.add_handler(CommandHandler("reviews", self.reviews))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("spec_ref", self.specify_refferal))
        application.add_handler(MessageHandler(filters.ALL, self.handle_message))

    def setup_keyboards(self):
        next_review_button = InlineKeyboardButton(
            text="➡️",
            callback_data="next_review"
        )

        last_review_button = InlineKeyboardButton(
            text="⬅️",
            callback_data="last_review"
        )

        self.keyboard_reviews = [[last_review_button, next_review_button]]

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == "last_review":
            await self.last_review(update, context)
        elif query.data == "next_review":
            await self.next_review(update, context)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

        reply_markup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,  # Кнопки подгоняются под размер экрана
            one_time_keyboard=False  # Клавиатура не скрывается после нажатия
        )

        await update.message.reply_text("\"Стриж и КО\"\n\n"
                                    "Привет! Рады видеть тебя здесь!\n"
                                    "Наша компания предоставляет услуги стрижки по очень выгодным ценам!\n"
                                    "Только у нас ты можешь пригласить друзей и получить бесплатные стрижки,\n"
                                    "Только у нас ты можешь попросить парикмахера выехать к тебе домой,\n"
                                    "А также именно у нас ты можешь получить бесплатные стрижки за частое посещение!\n\n"
                                    "Ждём тебя, наш парикмахер уже готовится!)",
            reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        user_id = user.id
        self.base_commands_db.add_user_to_db(user_id)


    async def price(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
       await update.message.reply_text("ПРАЙС\n\n"
                                      f"{self.base_commands_db.get_price()}\n")


    async def account(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        userID = user.id
        count = self.base_commands_db.get_count_haircuts(userID) % self.config_creator.get_config_value(
            "count_haircuts_to_free") if self.base_commands_db.get_count_haircuts(userID) != 0 else 3

        await update.message.reply_text(f"АККАУНТ\n\n"
                                    f"Количество стрижек у нас: {self.base_commands_db.get_count_haircuts(userID)}\n"
                                    f"Количество бесплатных стрижек: {self.base_commands_db.get_count_free_haircuts(userID)}\n\n"
                                    f"Реферальные баллы за приглашённых друзей: {self.base_commands_db.get_referral_coins(userID)}\n"
                                    f"Оставшееся количество стрижек для получения 1 бесплатной: {count}\n")

    async def referral(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"РЕФЕРАЛЬНАЯ СИСТЕМА\n\n"
                                    f"Пригласи друзей и получи реферальные баллы!\n"
                                    f"За каждого приведённого друга, прошедшего 3 платные стрижки ты получаешь 100 баллов.\n"
                                    f"300 баллов => 1 бесплатная стрижка!")

    async def specify_refferal(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"Укажите Username реферера (Пример: @Alexey_Popov)")

    async def add_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(f"ОСТАВИТЬ ОТЗЫВ\n\n"
                                    f"Пожалуйста, опишите, что вам понравилось/не понравилось на стрижке?")
        return self.REVIEW_TEXT


    async def review_text_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data['review_text'] = update.message.text
        await update.message.reply_text(f"ОСТАВИТЬ ОТЗЫВ\n\n"
                                    f"Оставьте оценку качеству (от 1 до 5)")
        return self.REVIEW_RATING


    async def review_rating_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        rating = update.message.text
        review_text = context.user_data.get('review_text', '')
        user_id = update.effective_user.id
        username = update.effective_user.username or f"user_{user_id}"

        if rating.isdigit() and 1 <= int(rating) <= 5:
            context.user_data.pop('review_text', None)
            is_review_added = self.base_commands_db.add_or_update_review(user_id, username, review_text, rating)
            status = "изменён"

            if is_review_added:
                status = "добавлен"

            await update.message.reply_text("Спасибо за ваш отзыв!\n"
                                            f"Текст: {review_text}\n"
                                            f"Оценка: {rating}/5\n\n"
                                            f"Отзыв успешно {status}!")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Пожалуйста, введите число от 1 до 5:")
            return self.REVIEW_RATING


    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.pop('review_text', None)
        await update.message.reply_text("Создание отзыва отменено.")
        return ConversationHandler.END

    async def reviews(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if context.user_data is None:
            context.user_data = {}
        if 'review_index' not in context.user_data:
            context.user_data['review_index'] = 0

        await self.send_review_text(update, context)

    async def send_review_text(self, update: Update,
                               context: ContextTypes.DEFAULT_TYPE) -> None:
        data = self.base_commands_db.get_review_by_index(context.user_data['review_index'])

        text = (f"ОТЗЫВЫ\n\n"
                f"Пользователь: {data[0]}\n"
                f"Отзыв: {data[1]}\n"
                f"Оценка: {data[2]}\n")

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(self.keyboard_reviews)
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(self.keyboard_reviews))

    async def next_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data['review_index'] + 1 > self.base_commands_db.get_count_reviews() - 1:
            context.user_data['review_index'] = 0
        else:
            context.user_data['review_index'] += 1

        await self.send_review_text(update, context)

    async def last_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data['review_index'] - 1 < 0:
            context.user_data['review_index'] = self.base_commands_db.get_count_reviews() - 1
        else:
            context.user_data['review_index'] -= 1

        await self.send_review_text(update, context)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"СУЩЕСТВУЮЩИЕ КОМАНДЫ\n\n"
                                        f"/start - Узнать основную информацию.\n"
                                        f"/price - Узнать прайс на стрижки.\n"
                                        f"/account - Посмотреть свой баланс и статистику.\n"
                                       f"/referral - Информация о реферальной системе.\n"
                                        f"/reviews - Посмотреть отзывы\n"
                                        f"/addreview - Оставить отзыв\n"
                                        f"/help - Показать это сообщение\n"
                                        f"/specRef - Указать реферера (Человека, который привел вас сюда)")