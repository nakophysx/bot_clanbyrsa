from uuid import uuid4
from time import sleep
from datetime import date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, Filters
from telegram.ext import CallbackQueryHandler, MessageHandler

###############################################################################
# ----------------------------- DATA STRUCTURES ----------------------------- #
###############################################################################


###############################################################################
# ---------------------------------- CMD ------------------------------------ #
###############################################################################


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""Estás inscrito correctamente en la base de datos del bot""")

###############################################################################
# ----------------------------- SUB-ROUTINES -------------------------------- #
###############################################################################


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="""Comando desconocido. Escribe /help para
                             recibir información adicional""")

###############################################################################
# ------------------------------- DICTIONARY -------------------------------- #
###############################################################################


cmd_dictionary = {'start': start, 'unknown': unknown}
