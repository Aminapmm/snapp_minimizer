from telegram.ext import Updater
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, \
    CallbackQueryHandler
from telegram import Update, ReplyKeyboardMarkup, ForceReply, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import os
#TOKEN = '1253801548:AAFoh-hSRvG-6ZxXsLvRpRssVFAVYPy2rT8'
TOKEN = os.environ['TELEGRAM_TOKEN']
bot_username = "@amineae772bot"

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

src_lat, src_long, dest_lat, dest_long = range(4)


def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Send Location", callback_data='0'),
                 InlineKeyboardButton("Enter Latitude/Longitude", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_user.send_message("Hello %s" % update.effective_chat.username)
    update.effective_user.send_message(text="Select One", reply_markup=reply_markup)
    print(update.effective_message)


def snap_price(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Origin", callback_data='0'),
                 InlineKeyboardButton("Destination", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_user.send_message(text="Select One", reply_markup=reply_markup)


def get_messages(update: Update, context: CallbackContext):

    if update.effective_message.reply_to_message.text == "Origin":
        context.user_data['origin'] = update.effective_message.text.split(",")

    elif update.effective_message.reply_to_message.text == "Destination":
        context.user_data['dest'] = update.effective_message.text.split(",")

    if ('origin' in context.user_data) and ('dest' in context.user_data):
        print("here")
        origin = context.user_data['origin']
        dest = context.user_data['dest']
        update.effective_user.send_message(
            "final price: %s \n src: %s , %s \n dest: %s , %s" % ('0', origin[0], origin[1], dest[0], dest[1]))

def get_location(update: Update, context: CallbackContext):
    update.effective_user.send_message("Gotcha!")
    print(update.effective_message)


def inline_button(update: Update, context: CallbackContext):
    query = update.callback_query

    location_keyboard = KeyboardButton(text="SEND ME YOUR LOCATION", request_location=True)
    reply_keyboard = ReplyKeyboardMarkup([[location_keyboard]], one_time_keyboard=True, resize_keyboard=True)

    if query.data == '0':
        query.edit_message_text(text="Selected option: Origin")
        update.effective_user.send_message(text="Origin", reply_markup=ForceReply(force_reply=True))
        # print(update.effective_message)

    if query.data == '1':
        query.edit_message_text(text="Selected option: Destination")
        update.effective_user.send_message(text="Destination", reply_markup=ForceReply(force_reply=True))

    # print(query.to_json())


start_handler = CommandHandler('start', start)
snap_price_handler = CommandHandler("SnapPrice", snap_price)
inline_button_handler = CallbackQueryHandler(inline_button)
msg_handler = MessageHandler(Filters.text, get_messages)
location_handler = MessageHandler(Filters.location, get_location)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(snap_price_handler)
dispatcher.add_handler(msg_handler)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(inline_button_handler)
updater.start_polling()
updater.idle()
