import byrsa_db as b_db
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
    b_db.new_rover(update.effective_user.id, update.effective_user.first_name)
    update.message.reply_text(
        "Te has inscrito correctamente en la base de datos del bot")


def asistencia(context, update):
    args = update.message.text.split()
    activity_info = ''
    for i in range(1, args.len()+1):
        activity_info += args[i]
    id = b_db.new_attendace_list(activity_info)
    keyboard = [[InlineKeyboardButton("Voy", callback_data='att-SI-'+str(id)),
                 InlineKeyboardButton("No voy",
                                      callback_data='att-NO-'+str(id)),
                 InlineKeyboardButton("Depende",
                                      callback_data='att-DEPENDE-'+str(id))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    attendance_text = b_db.get_attendance_text(update.message.chat.id,
                                               update.message.message_id)
    update.message.reply_text(attendance_text, reply_markup=reply_markup,
                              quote=True)


###############################################################################
# ----------------------------- SUB-ROUTINES -------------------------------- #
###############################################################################


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=("Comando desconocido. Escribe /help para "
                                   "recibir información adicional"))


def button(update, context):
    update.callback_query.answer()
    # data is a string shaped like this: "dict_key-argument0-argument1..."
    data = update.callback_query.data.split('-', 1)
    if data[0] in cmd_dictionary:
        cmd_dictionary[data[0]](update, context)
    else:
        sbr_dictionary[data[0]](update, context, data[1])


def add_participant(update, context, data):
    args = data.split('-')
    b_db.add_attendant(update.effective_user.id, args[1], args[0])

###############################################################################
# ------------------------------- DICTIONARY -------------------------------- #
###############################################################################


# Commands only need update and context arguments
cmd_dictionary = {}

# Subroutines need update, context and data (Empty str if not required)
sbr_dictionary = {'att': add_participant}
