from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os

_MAX_MESSAGE_SIZE = 4000


async def _run_with_response(cmd, bot, chat_id):
    resp = os.popen(cmd).read()

    await bot.send_message(chat_id=chat_id, text=f"Executed command:{cmd}, result:\n")
    for y in range(_MAX_MESSAGE_SIZE, len(resp) + _MAX_MESSAGE_SIZE, _MAX_MESSAGE_SIZE):
        await bot.send_message(chat_id=chat_id, text=resp[y-_MAX_MESSAGE_SIZE:y])


class Bot:
    def __init__(self, config, trigger_pause_listener):
        self.application = ApplicationBuilder().token(config['TelegramBotApiKey']).build()
        self.masterChatId = int(config['MasterChatId'])
        self.trigger_pause_listener = trigger_pause_listener

        self.application.add_handler(CommandHandler('light_pause', self.light_pause))
        self.application.add_handler(CommandHandler('light_resume', self.light_resume))
        self.application.add_handler(CommandHandler('command', self.command))
        self.application.add_handler(CommandHandler('cchmod', self.cchmod))
        self.application.add_handler(CommandHandler('clogs', self.clogs))
        self.application.add_handler(CommandHandler('deluge', self.deluge))

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

    async def command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_permission(update, context):
            return
        cmd = ' '.join(context.args)
        await _run_with_response(cmd, context.bot, update.effective_chat.id)

    async def cchmod(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_permission(update, context):
            return
        await _run_with_response("sudo chmod -R 777 /media/usb", context.bot, update.effective_chat.id)

    async def clogs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_permission(update, context):
            return
        await _run_with_response("journalctl --unit=pserver.service -n 100 --no-pager", context.bot,
                                 update.effective_chat.id)

    async def deluge(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_permission(update, context):
            return
        cmd = 'deluge-console ' + ' '.join(context.args)
        await _run_with_response(cmd, context.bot, update.effective_chat.id)

    def run(self):
        self.application.run_polling()

    async def _check_permission(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != self.masterChatId:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No permission")
            return False

        return True
