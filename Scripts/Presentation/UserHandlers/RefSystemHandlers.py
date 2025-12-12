from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from Scripts.Application.User.AddReferrerUseCase import AddReferrerUseCase
from Scripts.Application.User.GetHaircutDataUseCase import GetHaircutDataUseCase


class RefSystemHandlers:
    def __init__(self, get_tech_data_uc: GetHaircutDataUseCase,
                 add_referrer_uc: AddReferrerUseCase):
        self.get_tech_data_uc = get_tech_data_uc
        self.add_referrer_uc = add_referrer_uc

        self.REFERRER_TEXT = 0

    def setup_handlers(self, application):
        referral_conversation = ConversationHandler(
            entry_points=[
                CommandHandler("spec_ref", self.specify_referrer),
                MessageHandler(filters.Regex(r'^🤝'), self.specify_referrer)
            ],
            states={
                self.REFERRER_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.end_specify_referrer)],
            },
            fallbacks=[
                CommandHandler("cancel", self.cancel),
                MessageHandler(filters.COMMAND, self.cancel),
                MessageHandler(filters.Regex(r'^[\U0001F300-\U0001F9FF]'), self.cancel)
            ],
        )

        application.add_handler(referral_conversation, group=0)

        application.add_handler(MessageHandler(filters.Regex(r'^👥'), self.referral), group=1)

        application.add_handler(CommandHandler("referral", self.referral), group=1)

    async def referral(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        data = self.get_tech_data_uc.execute()
        ref_haircuts_to_bonus = data["count_referral_haircuts_to_bonus"]
        coins_for_referral = data["coins_for_one_referral"]
        coins_free_haircut = data["coins_for_free_haircut"]

        await update.message.reply_text(f"РЕФЕРАЛЬНАЯ СИСТЕМА\n\n"
                                        f"Пригласи друзей и получи реферальные баллы!\n"
                                        f"За каждого приведённого друга, прошедшего {ref_haircuts_to_bonus}"
                                        f"платных стрижкек ты получаешь {coins_for_referral} баллов.\n"
                                        f"{coins_free_haircut} баллов => 1 бесплатная стрижка!")

    async def specify_referrer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(f"Укажите Username реферера (Пример: @Alexey_Popov)")
        return self.REFERRER_TEXT

    async def end_specify_referrer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        referrer = update.message.text
        user_id = update.effective_user.id

        self.add_referrer_uc.execute(user_id, referrer)
        await update.message.reply_text(f"Реферер добавлен!")
        return self.REFERRER_TEXT

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.pop('review_text', None)
        await update.message.reply_text("Команда отменена.")
        return ConversationHandler.END
