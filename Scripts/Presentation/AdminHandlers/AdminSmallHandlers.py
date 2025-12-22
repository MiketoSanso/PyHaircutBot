from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from Scripts.Application.Admin.AddHaircutByUsernameUseCase import AddHaircutByUsernameUseCase
from Scripts.Application.Admin.SearchAdminUseCase import SearchAdminUseCase


class AdminSmallHandlers:
    def __init__(self, search_admin_uc: SearchAdminUseCase,
                 add_haircut_by_username_uc: AddHaircutByUsernameUseCase):
        self.add_haircut_by_username_uc = add_haircut_by_username_uc
        self.search_admin_uc = search_admin_uc

    def setup_handlers(self, application):
        application.add_handler(CommandHandler("admin_help", self.admin_help), group=1)
        application.add_handler(CommandHandler("add_haircut", self.add_haircut), group=1)

    async def admin_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if self.search_admin_uc.execute(user_id):
            await update.message.reply_text("Существующие команды для админа:\n\n"
                                            "Переменные для получения бесплатных стрижек.\n"
                                            "/change_coins_for_free_haircut (ЧИСЛО) - \n"
                                            "/change_coins_for_ref (ЧИСЛО) - \n"
                                            "/change_haircuts_to_free (ЧИСЛО) - \n"
                                            "/change_ref_haircuts_to_bonus (ЧИСЛО) - \n\n"
                                            "Команды для управления системой админов."
                                            "/change_admin_password (ТЕКСТ) - Сменить пароль для системы админов.\n"
                                            "/add_admin_by_id (ID) - Добавить администратора.\n"
                                            "/verify_admin_status (ПАРОЛЬ) - Залогиниться как админ.\n"
                                            "/delete_admin (ID) - удалить админа\n\n"
                                            "Команды управления пользователями."
                                            "/add_haircut (USERNAME) - Добавить пользователю стрижку."
                                            "/admin_help - Увидеть это сообщение.")
        else:
            await update.message.reply_text("Команда недоступна.")


    async def add_haircut(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите Username\n"
                "Например: /change_admin_password @Miketo_Sanso"
            )
            return

        username = str(context.args[0])
        print(username)

        if username.startswith('@'):
            username = username[1:]
        user_id = update.effective_user.id

        is_changed = self.add_haircut_by_username_uc.execute(user_id, username)

        if is_changed:
            await update.message.reply_text(f"Стрижка добавлена успешно!")
        else:
            await update.message.reply_text(f"Произошла ошибка при добавлении стрижки!")
