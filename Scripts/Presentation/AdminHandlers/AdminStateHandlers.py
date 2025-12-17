from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from Scripts.Application.Admin.AddAdminByIdUseCase import AddAdminByIdUseCase
from Scripts.Application.Admin.AddAdminByPasswordUseCase import AddAdminByPasswordUseCase
from Scripts.Application.Admin.ChangeAdminPasswordUseCase import ChangeAdminPasswordUseCase
from Scripts.Application.Admin.RemoveAdminUseCase import RemoveAdminUseCase


class AdminStateHandlers:

    def __init__(self,
                 add_admin_by_id_uc: AddAdminByIdUseCase,
                 add_admin_by_password_uc: AddAdminByPasswordUseCase,
                 remove_admin_uc: RemoveAdminUseCase,
                 change_admin_password_uc: ChangeAdminPasswordUseCase):
        self.change_admin_password_uc = change_admin_password_uc
        self.add_admin_by_id_uc = add_admin_by_id_uc
        self.add_admin_by_password_uc = add_admin_by_password_uc
        self.remove_admin_uc = remove_admin_uc

    def setup_handlers(self, application):
        application.add_handler(CommandHandler("change_admin_password", self.change_admin_password), group=1)
        application.add_handler(CommandHandler("add_admin_by_id", self.add_admin_by_id), group=1)
        application.add_handler(CommandHandler("verify_admin_status", self.verify_admin_status), group=1)
        application.add_handler(CommandHandler("delete_admin", self.delete_admin), group=1)

    async def change_admin_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите пароль\n"
                "Например: /change_admin_password newPassword"
            )
            return

        new_password = str(context.args[0])
        user_id = update.effective_user.id

        is_changed = self.change_admin_password_uc.execute(user_id, new_password)

        if is_changed:
            await update.message.reply_text(f"Пароль успешно изменён!")
        else:
            await update.message.reply_text(f"Произошла ошибка при смене пароля!")

    async def add_admin_by_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите ID пользователя\n"
                "Например: /add_admin_by_id 1000"
            )
            return

        try:
            admin_id = int(context.args[0])
            user_id = update.effective_user.id

            is_added = self.add_admin_by_id_uc.execute(user_id, admin_id)
            await self.__write_end_text(update, is_added, "добавлен", "добавлении")

        except ValueError:
            await update.message.reply_text("ID должен быть числом!")

    async def verify_admin_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите пароль\n"
                "Например: /verify_admin_status adminPassword"
            )
            return

        password = str(context.args[0])
        user_id = update.effective_user.id

        is_added = self.add_admin_by_password_uc.execute(user_id, password)
        await self.__write_end_text(update, is_added, "добавлен", "добавлении")

    async def delete_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите ID пользователя\n"
                "Например: /add_admin_by_id 1000"
            )
            return

        try:
            admin_id = int(context.args[0])
            user_id = update.effective_user.id

            is_removed = self.remove_admin_uc.execute(user_id, admin_id)
            await self.__write_end_text(update, is_removed, "удалён", "удалении")

        except ValueError:
            await update.message.reply_text("ID должен быть числом!")

    async def __write_end_text(self, update: Update, state: bool, deal_1: str, deal_2: str):
        if state:
            await update.message.reply_text(f"Администратор успешно {deal_1}!")
        else:
            await update.message.reply_text(f"Произошла ошибка при {deal_2} администратора!")
