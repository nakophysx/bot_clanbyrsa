import byrsa_db as b_db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize

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


def help(update, context):
    update.message.reply_text("Usa /asistencia para crear una nueva lista")


def asistencia(update, context):
    args = update.message.text.split()
    if (len(args) >= 2):
        activity_info = ''
        for i in range(1, args.len()+1):
            activity_info += args[i]
    else:
        activity_info = 'ACB'

    id = b_db.new_attendace_list(activity_info)
    print("new list created named:" + activity_info)
    keyboard = [[InlineKeyboardButton(emojize(":thumbs_up:"),
                                      callback_data='att-SI-'+str(id)),
                 InlineKeyboardButton(emojize(":question:"),
                                      callback_data='att-DEPENDE-'+str(id)),
                 InlineKeyboardButton(emojize(":-1:"),
                                      callback_data='att-NO-'+str(id))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    attendance_text = b_db.get_attendance_text(id)
    print(attendance_text)
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
    attendance_text = b_db.get_attendance_text(args[1])
    update.callback_query.edit_message_text(attendance_text)

###############################################################################
# ------------------------------- DICTIONARY -------------------------------- #
###############################################################################


# Commands only need update and context arguments
cmd_dictionary = {}

# Subroutines need update, context and data (Empty str if not required)
sbr_dictionary = {'att': add_participant}
