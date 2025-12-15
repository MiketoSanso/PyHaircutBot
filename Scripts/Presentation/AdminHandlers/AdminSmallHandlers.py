from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from Scripts.Application.Admin.SearchAdminUseCase import SearchAdminUseCase


class AdminSmallHandlers:
    def __init__(self, search_admin_uc: SearchAdminUseCase):
        self.search_admin_uc = search_admin_uc

    def setup_handlers(self, application):
        application.add_handler(CommandHandler("referral", self.referral), group=1)

    async def admin_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if self.search_admin_uc.execute(user_id):
            await update.message.reply_text("Существующие команды для админа:\n"
                                            "")
        else:
            await update.message.reply_text("Команда недоступна.")

    async def add_haircut_by_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
