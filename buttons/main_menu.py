from telegram import KeyboardButton, ReplyKeyboardMarkup
import globals
from fastfood_db import Database

db = Database()


async def main_menu(context,chat_id,lang_id,message_id=None):
    buttons = [
        [KeyboardButton(text=globals.BTN_ORDER[lang_id])],
        [KeyboardButton(text=globals.BTN_MY_ORDERS[lang_id]), KeyboardButton(text=globals.BTN_ABOUT_US[lang_id])],
        [KeyboardButton(text=globals.BTN_COMMENTS[lang_id]), KeyboardButton(text=globals.BTN_SETTINGS[lang_id])]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    if message_id:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=reply_markup
        )
