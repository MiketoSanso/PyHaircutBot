from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from Scripts.Infrastructure.UserRequests.AccountRequests import BaseCommands
from Scripts.Utils.ConfigCreator import ConfigCreator


class RefSystemCommands:
    def __init__(self, base_commands_db: BaseCommands,
                 config_creator: ConfigCreator):
        self.config_creator = config_creator
        self.base_commands_db = base_commands_db

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
                MessageHandler(filters.COMMAND, self.cancel)
            ],
        )

        application.add_handler(referral_conversation)

        application.add_handler(MessageHandler(filters.Regex(r'^👥'), self.referral))

        application.add_handler(CommandHandler("referral", self.referral))

    async def referral(self, update: Update) -> None:
        await update.message.reply_text(f"РЕФЕРАЛЬНАЯ СИСТЕМА\n\n"
                                        f"Пригласи друзей и получи реферальные баллы!\n"
                                        f"За каждого приведённого друга, прошедшего {self.config_creator.get_config_value("count_referral_haircuts_to_bonus")} "
                                        f"платных стрижкек ты получаешь {self.config_creator.get_config_value("coins_for_one_referral")} баллов.\n"
                                        f"{self.config_creator.get_config_value("coins_for_free_haircut")} баллов => 1 бесплатная стрижка!")

    async def specify_referrer(self, update: Update) -> int:
        await update.message.reply_text(f"Укажите Username реферера (Пример: @Alexey_Popov)")
        return self.REFERRER_TEXT

    async def end_specify_referrer(self, update: Update) -> int:
        referrer = update.message.text
        user_id = update.effective_user.id

        self.base_commands_db.add_referrer(user_id, referrer)
        await update.message.reply_text(f"Реферер добавлен!")
        return self.REFERRER_TEXT

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.pop('review_text', None)
        await update.message.reply_text("Команда отменена.")
        return ConversationHandler.END