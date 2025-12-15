from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from Scripts.Application.Admin.ChangeCoinsForFreeHaircutUseCase import ChangeCoinsForFreeHaircutUseCase
from Scripts.Application.Admin.ChangeCoinsForRefUseCase import ChangeCoinsForRefUseCase
from Scripts.Application.Admin.ChangeHaircutsToFreeUseCase import ChangeHaircutsToFreeUseCase
from Scripts.Application.Admin.ChangeRefHaircutsToBonusUseCase import ChangeRefHaircutsToBonusUseCase


class ChangeHaircutConfigHandlers:

    def __init__(self,
                 change_coins_for_free_haircut_uc: ChangeCoinsForFreeHaircutUseCase,
                 change_coins_for_ref_uc: ChangeCoinsForRefUseCase,
                 change_haircuts_to_free_uc: ChangeHaircutsToFreeUseCase,
                 change_ref_haircuts_to_bonus_uc: ChangeRefHaircutsToBonusUseCase):
        self.change_coins_for_free_haircut_uc = change_coins_for_free_haircut_uc
        self.change_coins_for_ref_uc = change_coins_for_ref_uc
        self.change_haircuts_to_free_uc = change_haircuts_to_free_uc
        self.change_ref_haircuts_to_bonus_uc = change_ref_haircuts_to_bonus_uc

    def setup_handlers(self, application):
        application.add_handler(CommandHandler("referral", self.referral), group=1)

    async def change_coins_for_free_haircut(self,
                                            update: Update,
                                            context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите число\n"
                "Например: /change_coins_for_free_haircut 500"
            )
            return

        try:
            haircut_for_free_haircut = int(context.args[0])

            is_changed = self.change_coins_for_free_haircut_uc.execute(haircut_for_free_haircut)

            await self.__write_end_text(update, is_changed)
        except ValueError:
            await update.message.reply_text("Параметр должен быть числом!")

    async def change_coins_for_ref(self,
                                   update: Update,
                                   context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите число\n"
                "Например: /change_coins_for_ref 500"
            )
            return

        try:
            coins_for_ref = int(context.args[0])

            is_changed = self.change_coins_for_ref_uc.execute(coins_for_ref)

            await self.__write_end_text(update, is_changed)
        except ValueError:
            await update.message.reply_text("Параметр должен быть числом!")

    async def change_haircuts_to_free(self,
                                      update: Update,
                                      context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите число\n"
                "Например: /change_haircuts_to_free 500"
            )
            return

        try:
            count_haircuts_to_free = int(context.args[0])

            is_changed = self.change_haircuts_to_free_uc.execute(count_haircuts_to_free)

            await self.__write_end_text(update, is_changed)
        except ValueError:
            await update.message.reply_text("Параметр должен быть числом!")

    async def change_ref_haircuts_to_bonus(self,
                                           update: Update,
                                           context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите число\n"
                "Например: /change_ref_haircuts_to_bonus 500"
            )
            return

        try:
            ref_haircuts_to_bonus = int(context.args[0])

            is_changed = self.change_ref_haircuts_to_bonus_uc.execute(ref_haircuts_to_bonus)

            await self.__write_end_text(update, is_changed)
        except ValueError:
            await update.message.reply_text("Параметр должен быть числом!")

    async def __write_end_text(self, update: Update, state: bool):
        if state:
            await update.message.reply_text(f"Значение успешно обновлено!")
        else:
            await update.message.reply_text(f"Значение не обновлено, задача завершилась с ошибкой!\n"
                                            f"Попробуйте уменьшить/увеличить число.")