import byrsa_commands as b_cmd
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request
import logging
import telegram.bot
from telegram.ext import messagequeue as mq
import os
TOKEN = os.environ.get('TOKEN')

###############################################################################
# --------------------------- ANTI-FLOOD CLASS------------------------------- #
###############################################################################


class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except Exception:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(*args, **kwargs)

###############################################################################
# ---------------------------- INITIALIZATION ------------------------------- #
###############################################################################


message_bot = MQBot(TOKEN,
                    request=Request(con_pool_size=8), mqueue=mq.MessageQueue())
updater = Updater(bot=message_bot, use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

###############################################################################
# ------------------------------- HANDLERS ---------------------------------- #
###############################################################################


print("Adding handlers...")
# Command Handlers
dispatcher.add_handler(CommandHandler('start', b_cmd.start))
dispatcher.add_handler(CommandHandler('help', b_cmd.help))
dispatcher.add_handler(CommandHandler('asistencia', b_cmd.asistencia))
# Unknown command handler
dispatcher.add_handler(MessageHandler(Filters.command, b_cmd.unknown))

print("Bot initialization went flawless. Polling updates...")
updater.start_polling()
