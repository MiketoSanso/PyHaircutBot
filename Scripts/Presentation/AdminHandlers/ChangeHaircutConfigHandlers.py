from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from Scripts.Application.User.AddUserUseCase import AddUserUseCase
from Scripts.Application.User.GetPriceUseCase import GetPriceUseCase
from Scripts.Application.User.GetUserDataUseCase import GetUserDataUseCase


class ChangeHaircutConfigHandlers:

    def __init__(self):
        pass

    def change_coins_for_free_haircut(self, application):
        pass

    def ChangeCoinsForRefUseCase(self):
        pass

    async def ChangeHaircutsToFree(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass

    async def ChangeRefHaircutsToBonus(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass

    async def price(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass

    async def account(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass