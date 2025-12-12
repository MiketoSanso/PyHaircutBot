from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, \
    CallbackQueryHandler
from Scripts.Application.User.GetCountReviewsUseCase import GetCountReviewsUseCase
from Scripts.Application.User.GetReviewByIndexUseCase import GetReviewByIndexUseCase
from Scripts.Application.User.UpsertReviewUseCase import UpsertReviewUseCase


class ReviewHandlers:
    def __init__(self,
                 upsert_review_uc: UpsertReviewUseCase,
                 get_review_by_index_uc: GetReviewByIndexUseCase,
                 get_count_reviews_uc: GetCountReviewsUseCase):
        self.keyboard_reviews = None
        self.get_count_reviews_uc = get_count_reviews_uc
        self.get_review_by_index_uc = get_review_by_index_uc
        self.upsert_review_uc = upsert_review_uc
        self.REVIEW_TEXT, self.REVIEW_RATING = range(2)

        self.setup_keyboards()

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
            fallbacks=[
                CommandHandler("cancel", self.cancel),
                MessageHandler(filters.COMMAND, self.cancel),
                MessageHandler(filters.Regex(r'^[\U0001F300-\U0001F9FF]'), self.cancel)
            ],
        )

        application.add_handler(review_conversation, group=0)
        application.add_handler(CallbackQueryHandler(self.button_handler), group=0)

        application.add_handler(MessageHandler(filters.Regex(r'^⭐'), self.reviews), group=1)

        application.add_handler(CommandHandler("reviews", self.reviews), group=1)

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
        estimation = update.message.text
        review_text = context.user_data.get('review_text', '')
        user_id = update.effective_user.id
        username = update.effective_user.username or f"user_{user_id}"

        if estimation.isdigit() and 1 <= int(estimation) <= 5:
            context.user_data.pop('review_text', None)
            is_review_added = self.upsert_review_uc.execute(user_id, username, review_text, estimation)
            status = "изменён"

            if is_review_added:
                status = "добавлен"

            await update.message.reply_text("Спасибо за ваш отзыв!\n"
                                            f"Текст: {review_text}\n"
                                            f"Оценка: {estimation}/5\n\n"
                                            f"Отзыв успешно {status}!")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Пожалуйста, введите число от 1 до 5:")
            return self.REVIEW_RATING

    async def reviews(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if context.user_data is None:
            context.user_data = {}
        if 'review_index' not in context.user_data:
            context.user_data['review_index'] = 0

        await self.send_review_text(update, context)

    async def send_review_text(self, update: Update,  context: ContextTypes.DEFAULT_TYPE) -> None:
        data = self.get_review_by_index_uc.execute(context.user_data['review_index'])

        if data is None:
            await update.message.reply_text("Отзывов пока нет! Будьте первыми :D")
            return

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
        if self.get_count_reviews_uc.execute() - 1 == 0:
            return
        elif context.user_data['review_index'] + 1 > self.get_count_reviews_uc.execute() - 1:
            context.user_data['review_index'] = 0
        else:
            context.user_data['review_index'] += 1

        await self.send_review_text(update, context)

    async def last_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.get_count_reviews_uc.execute() - 1 == 0:
            return
        elif context.user_data['review_index'] - 1 < 0:
            context.user_data['review_index'] = self.get_count_reviews_uc.execute() - 1
        else:
            context.user_data['review_index'] -= 1

        await self.send_review_text(update, context)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.pop('review_text', None)
        await update.message.reply_text("Команда отменена.")
        return ConversationHandler.END