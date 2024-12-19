from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import globals

from fastfood_db import Database

db = Database()


async def start_conv(update, context):
    user = update.message.from_user
    buttons = [
        [KeyboardButton(text=globals.BTN_LANG_UZ)],
        [KeyboardButton(text=globals.BTN_LANG_RU)]
    ]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text=globals.WELCOME_TEXT)
    await update.message.reply_text(
        text=globals.CHOOSE_LANG,
        reply_markup=reply_markup
    )
    return "CHOOSE_LANG"


async def choose_lang(update, context):
    message = update.message.text
    if message == globals.BTN_LANG_UZ:
        lang_id = 1
        context.user_data["lang_id"] = lang_id
        await update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[lang_id],
            reply_markup=ReplyKeyboardRemove()
        )
        return "FIRST_NAME"

    elif message == globals.BTN_LANG_RU:
        lang_id = 2
        context.user_data["lang_id"] = lang_id
        await update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[lang_id],
            reply_markup=ReplyKeyboardRemove()
        )
        return "FIRST_NAME"

    else:
        await update.message.reply_text(text=globals.TEXT_LANG_WARNING)
        return "CHOOSE_LANG"


async def enter_first_name(update, context):
    first_name = update.message.text
    lang_id = context.user_data["lang_id"]
    context.user_data["first_name"] = first_name
    await update.message.reply_text(
        text=globals.TEXT_ENTER_LAST_NAME[lang_id]
    )
    return "LAST_NAME"

async def enter_last_name(update, context):
    last_name = update.message.text
    lang_id = context.user_data["lang_id"]
    context.user_data["last_name"] = last_name
    button = [
        [KeyboardButton(text=globals.BTN_SEND_CONTACT[lang_id])]
    ]
    reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        text=globals.TEXT_ENTER_CONTACT[lang_id],
        reply_markup=reply_markup
    )
