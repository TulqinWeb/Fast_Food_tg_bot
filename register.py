from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
import globals
from fastfood_db import Database
import logging

db = Database()

# STATES
CHOOSE_LANG, FIRST_NAME, LAST_NAME, CONTACT = range(4)


async def start_conv(update, context):
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    if db_user:
        lang_id = db_user["lang_id"]
        await update.message.reply_text(text=globals.TEXT_MAIN_MENU[lang_id])
        return ConversationHandler.END
    else:
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
        return CHOOSE_LANG


async def choose_lang(update, context):
    message = update.message.text
    print(message)
    logging.info(f"Foydalanuvhi tanlovi {message}")
    if message == globals.BTN_LANG_UZ:
        lang_id = 1
        context.user_data["lang_id"] = lang_id
        await update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[lang_id],
            reply_markup=ReplyKeyboardRemove()
        )
        return FIRST_NAME

    elif message == globals.BTN_LANG_RU:
        lang_id = 2
        context.user_data["lang_id"] = lang_id
        await update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[lang_id],
            reply_markup=ReplyKeyboardRemove()
        )
        return FIRST_NAME

    else:
        await update.message.reply_text(text=globals.TEXT_LANG_WARNING)
        return CHOOSE_LANG


async def enter_first_name(update, context):
    first_name = update.message.text
    lang_id = context.user_data["lang_id"]
    context.user_data["first_name"] = first_name
    await update.message.reply_text(
        text=globals.TEXT_ENTER_LAST_NAME[lang_id]
    )
    return LAST_NAME


async def enter_last_name(update, context):
    last_name = update.message.text
    lang_id = context.user_data["lang_id"]
    context.user_data["last_name"] = last_name
    button = [
        [KeyboardButton(
            text=globals.BTN_SEND_CONTACT[lang_id],
            request_contact=True
        )]
    ]
    reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        text=globals.TEXT_ENTER_CONTACT[lang_id],
        reply_markup=reply_markup
    )
    return CONTACT


async def enter_contact(update, context):
    contact = update.message.contact
    lang_id = context.user_data["lang_id"]
    if contact and contact.phone_number:
        phone_number = contact.phone_number
        context.user_data["phone_number"] = phone_number

        await update.message.reply_text(
            text=globals.TEXT_MAIN_MENU[lang_id],
            reply_markup=ReplyKeyboardRemove()
        )

        # Save data to Database
        user_data = context.user_data
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        phone_number = user_data.get("phone_number")
        chat_id = update.message.from_user.id

        db.create_user(first_name, last_name, phone_number, lang_id, chat_id)
        return ConversationHandler.END

    else:
        await update.message.reply_text(
            text=globals.TEXT_ENTER_CONTACT[lang_id]
        )
        return CONTACT


async def fallbacks(update, context):
    lang_id = context.user_data.get("lang_id")
    await update.message.reply_text(text=globals.FALLBACK[lang_id])
    return ConversationHandler.END
