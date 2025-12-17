from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

from Scripts.Application.Admin.GetQrUseCase import GetQrUseCase
from Scripts.Application.Admin.GetReferencesUseCase import GetReferencesUseCase
from Scripts.Application.User.AddUserUseCase import AddUserUseCase
from Scripts.Application.User.GetPriceUseCase import GetPriceUseCase
from Scripts.Application.User.UserData.GetUserFreeHaircutsUseCase import GetUserFreeHaircutsUseCase
from Scripts.Application.User.UserData.GetUserHaircutsToFreeUseCase import GetUserHaircutsToFreeUseCase
from Scripts.Application.User.UserData.GetUserHaircutsUseCase import GetUserHaircutsUseCase
from Scripts.Application.User.UserData.GetUserReferralCoinsUseCase import GetUserReferralCoinsUseCase


class UserSmallHandlers:

    def __init__(self,
                 get_user_free_haircuts_uc: GetUserFreeHaircutsUseCase,
                 get_user_haircuts_uc: GetUserHaircutsUseCase,
                 get_user_referral_coins_uc: GetUserReferralCoinsUseCase,
                 get_user_haircuts_to_free_uc: GetUserHaircutsToFreeUseCase,
                 add_user_use_case: AddUserUseCase,
                 get_price_use_case: GetPriceUseCase,
                 get_qr_uc: GetQrUseCase,
                 get_references_uc: GetReferencesUseCase):
        self.get_qr_uc = get_qr_uc
        self.get_references_uc = get_references_uc
        self.get_user_free_haircuts_uc = get_user_free_haircuts_uc
        self.get_user_haircuts_to_free_uc = get_user_haircuts_to_free_uc
        self.get_user_referral_coins_uc = get_user_referral_coins_uc
        self.get_user_haircuts_uc = get_user_haircuts_uc
        self.get_price_use_case = get_price_use_case
        self.add_user_use_case = add_user_use_case
        self.reply_keyboard = None

    def setup_handlers(self, application):
        application.add_handler(MessageHandler(filters.ALL, self.handle_message), group=2)

        application.add_handler(MessageHandler(filters.Regex(r'^👾'), self.start), group=1)
        application.add_handler(MessageHandler(filters.Regex(r'^🖼️'), self.show_work_references), group=1)
        application.add_handler(MessageHandler(filters.Regex(r'^💼'), self.show_qr_pay), group=1)
        application.add_handler(MessageHandler(filters.Regex(r'^💰'), self.price), group=1)
        application.add_handler(MessageHandler(filters.Regex(r'^👤'), self.account), group=1)
        application.add_handler(MessageHandler(filters.Regex(r'^❓'), self.help_command), group=1)

        application.add_handler(CommandHandler("start", self.start), group=1)
        application.add_handler(CommandHandler("references", self.show_work_references), group=1)
        application.add_handler(CommandHandler("qr_pay", self.show_qr_pay), group=1)
        application.add_handler(CommandHandler("price", self.price), group=1)
        application.add_handler(CommandHandler("account", self.account), group=1)
        application.add_handler(CommandHandler("help", self.help_command), group=1)

    def _setup_keyboards(self):
        keyboard = [
            ["👾 Начать работу с ботом"],
            ["💰 Прайс"],
            ["🖼️ Примеры работ"],
            ["👤 Аккаунт"],
            ["⭐ Посмотреть отзывы"],
            ["🏅 Оставить отзыв"],
            ["💼 QR оплаты"],
            ["❓ Помощь"],
            ["👥 Реферальная система"],
            ["🤝 Добавить реферала"]
        ]

        self.reply_keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=False,
            one_time_keyboard=False
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("\"Твой личный парикмахер\"\n\n"
                                        "Привет! Рад видеть тебя здесь!\n"
                                        "Моя компания предоставляет услуги стрижки по очень выгодным ценам!\n"
                                        "Только у нас ты можешь пригласить друзей и получить бесплатные стрижки,\n"
                                        "Только у нас ты можешь попросить парикмахера выехать к тебе домой,\n"
                                        "А также именно у нас ты можешь получить "
                                        "бесплатные стрижки за частое посещение!\n\n"
                                        "Ждём тебя, наш парикмахер уже готовится!)",
                                        reply_markup=self.reply_keyboard
                                        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        user_id = user.id
        username = user.username if user.username is not None else "user_" + str(user.id)
        self.add_user_use_case.execute(user_id, username)
        self._setup_keyboards()
        return

    async def price(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("ПРАЙС\n\n"
                                        f"{self.get_price_use_case.execute()}\n")

    async def account(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        user_id = user.id

        data = [
            self.get_user_haircuts_uc.execute(user_id),
            self.get_user_free_haircuts_uc.execute(user_id),
            self.get_user_referral_coins_uc.execute(user_id),
            self.get_user_haircuts_to_free_uc.execute(user_id),
        ]
        await update.message.reply_text(f"АККАУНТ\n\n"
                                        f"Количество стрижек у нас: {data[0]}\n"
                                        f"Количество бесплатных стрижек: {data[1]}\n\n"
                                        f"Реферальные баллы за приглашённых друзей: {data[2]}\n"
                                        f"Оставшееся количество стрижек для получения 1 бесплатной: {data[3]}\n")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"СУЩЕСТВУЮЩИЕ КОМАНДЫ\n\n"
                                        f"/start - Узнать основную информацию.\n"
                                        f"/price - Узнать прайс на стрижки.\n"
                                        f"/references - Посмотреть примеры работ\n"
                                        f"/account - Посмотреть свой баланс и статистику.\n"
                                        f"/referral - Информация о реферальной системе.\n"
                                        f"/reviews - Посмотреть отзывы.\n"
                                        f"/add_review - Оставить отзыв.\n"
                                        f"/qr_pay - Показать QR оплаты.\n"
                                        f"/help - Показать это сообщение.\n"
                                        f"/spec_ref - Указать реферера (Человека, который привел вас сюда).")

    async def show_qr_pay(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        photo_paths = self.get_qr_uc.execute()
        await self.load_images(photo_paths, update, context)


    async def show_work_references(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        photo_paths = self.get_references_uc.execute()
        await self.load_images(photo_paths, update, context)

    async def load_images(self, photo_paths: list[str], update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Подождите...")

        if not photo_paths:
            await update.message.reply_text("Пока тут ничего нет!")
            return

        media_group = []
        for i, photo_path in enumerate(photo_paths, 1):
            with open(photo_path, 'rb') as photo_file:
                media_group.append(
                    InputMediaPhoto(
                        media=photo_file
                    )
                )

        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=media_group
        )