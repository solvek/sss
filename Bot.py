from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


class Bot:
    def __init__(self, config, trigger_pause_listener):
        self.application = ApplicationBuilder().token(config['TelegramBotApiKey']).build()
        self.masterChatId = config['MasterChatId']
        self.trigger_pause_listener = trigger_pause_listener

        self.application.add_handler(CommandHandler('light_pause', self.light_pause))
        self.application.add_handler(CommandHandler('light_resume', self.light_resume))

    async def send_message(self, message, chat_id=None):
        if chat_id is None:
            chat_id = self.masterChatId

        await self.application.bot.send_message(text=message, chat_id=chat_id)

    async def light_pause(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await self._check_permission(update, context):
            self.trigger_pause_listener(True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Light tracking paused")

    async def light_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await self._check_permission(update, context):
            self.trigger_pause_listener(False)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Light tracking resumed")

    def run(self):
        self.application.run_polling()

    async def _check_permission(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != self.masterChatId:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No permission")
            return False

        return True
