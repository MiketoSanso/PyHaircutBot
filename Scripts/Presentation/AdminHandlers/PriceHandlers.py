from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

from Scripts.Application.Admin.DeleteService import DeleteService
from Scripts.Application.Admin.GetCountServices import GetCountServices


class PriceHandlers:
    def __init__(self,
                 get_count_services_uc: GetCountServices,
                 delete_service_uc: DeleteService):
        self.delete_service_uc = delete_service_uc
        self.get_count_services_uc = get_count_services_uc
        self.POINT_NAME, self.POINT_COST, self.POINT_NUMBER, self.POINT_END = 0, 1, 2, 3

    def setup_handlers(self, application):
        add_point_conversation = ConversationHandler(
            entry_points=[
                CommandHandler("add_price_point", self.select_service_name),
            ],
            states={
                self.POINT_COST: [MessageHandler(filters.TEXT & ~filters.COMMAND &
                                                    ~filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'),
                                                    self.select_service_cost)],
                self.POINT_END: [MessageHandler(filters.TEXT & ~filters.COMMAND &
                                                 ~filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'),
                                                 self.end_adding)]
            },
            fallbacks=[
                CommandHandler("cancel", self.cancel),
                MessageHandler(filters.COMMAND, self.cancel),
                MessageHandler(filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'), self.cancel)
            ],
        )

        change_point_conversation = ConversationHandler(
            entry_points=[
                CommandHandler("change_price_point", self.select_service_number),
            ],
            states={
                self.POINT_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND &
                                                    ~filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'),
                                                    self.select_service_number)],
                self.POINT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND &
                                                    ~filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'),
                                                    self.select_service_name)],
                self.POINT_COST: [MessageHandler(filters.TEXT & ~filters.COMMAND &
                                                 ~filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'),
                                                 self.select_service_cost)],
                self.POINT_END: [MessageHandler(filters.TEXT & ~filters.COMMAND &
                                                 ~filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'),
                                                 self.end_changing)]
            },
            fallbacks=[
                CommandHandler("cancel", self.cancel),
                MessageHandler(filters.COMMAND, self.cancel),
                MessageHandler(filters.Regex(r'^(🤝|👥|🏅|⭐|➡️|⬅️|👾|💰|👤|❓|🖼️|💼)'), self.cancel)
            ],
        )

        application.add_handler(add_point_conversation, group=0)
        application.add_handler(change_point_conversation, group=0)


    async def select_service_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['mode'] = "change"
        await update.message.reply_text("Укажите номер сервиса, который хотите изменить:")
        return self.POINT_NAME

    async def select_service_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data['mode'] == "change":
            number = update.message.text
            count_services = self.get_count_services_uc.execute()
            if number is int and number > 0 and number < count_services:
                context.user_data['point_number'] = update.message.text
            else:
                if number is not int and number:
                    await update.message.reply_text("Укажите номер числом!, который хотите изменить.")
                elif number > 0 and number < count_services:
                    await update.message.reply_text("Вы указали неверное число!")
                else:
                    await update.message.reply_text("Сервисов ещё нету, нечего менять!")
                    return ConversationHandler.END

            return self.POINT_NAME

        await update.message.reply_text("Укажите название сервиса:")

        return self.POINT_COST

    async def select_service_cost(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['service_name'] = update.message.text
        await update.message.reply_text("Укажите цену сервиса:")
        return self.POINT_END

    async def end_adding(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        service_cost = update.message.text
        if service_cost is not int or service_cost < 0 or service_cost > 10000:
            await update.message.reply_text("Вы ввели невалидное число! Попробуйте ещё раз.")
            return self.POINT_END


        return ConversationHandler.END

    async def end_changing(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        service_cost = update.message.text
        if service_cost is not int or service_cost < 0 or service_cost > 10000:
            await update.message.reply_text("Вы ввели невалидное число! Попробуйте ещё раз.")
            return self.POINT_END


        return ConversationHandler.END

    async def delete_service_by_index(self, update: Update, context: ContextTypes.DEFAULT_TYPE, index):
        count_services = self.get_count_services_uc.execute()
        if count_services == 0:
            await update.message.reply_text("Ещё нету ни одного сервиса, нечего удалять!")
            return

        if not context.args or len(context.args) == 0:
            await update.message.reply_text(
                "Пожалуйста, укажите число\n"
                "Например: /delete_service_by_index 2"
            )
            return

        try:
            index = int(context.args[0])
            if index < 0 or index > count_services:
                await update.message.reply_text("Индекс неверный!")
                return

            is_deleted = self.delete_service_uc.execute(index)
            if not is_deleted:
                await update.message.reply_text("Параметр должен быть числом!")

        except ValueError:
            await update.message.reply_text("Параметр должен быть числом!")

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.pop('service_name', None)
        context.user_data.pop('mode', None)
        context.user_data.pop('point_number', None)

        await update.message.reply_text("Команда отменена.")
        return ConversationHandler.END