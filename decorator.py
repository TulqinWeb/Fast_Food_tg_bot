from telegram import KeyboardButton, ReplyKeyboardMarkup
import globals
from fastfood_db import Database

db = Database()


def check_user_data():
    def decorator(func):
        async def wrapper(update, context, *args, **kwargs):
            user = update.message.from_user
            db_user = db.get_user_by_chat_id(user.id)

            if not db_user or not db_user["lang_id"]:
                await dec_choose_lang(update, context)
                return
            if not db_user["first_name"]:
                await update.message.reply_text(
                    text=globals.TEXT_ENTER_FIRST_NAME[db_user["lang_id"]]
                )
                context.user_data["missing_field"] = "first_name"
                return
            if not db_user["last_name"]:
                await update.message.reply_text(
                    text=globals.TEXT_ENTER_LAST_NAME[db_user["lang_id"]]
                )
                context.user_data["missing_field"] = "last_name"
                return
            if not db_user["phone_number"]:
                await dec_enter_contact(update, context)
                context.user_data["missing_field"] = "phone_number"
                return

            return await func(update, context, *args, **kwargs)

        return wrapper

    return decorator


async def dec_choose_lang(update, context):
    buttons = [
        [KeyboardButton(text=globals.BTN_LANG_UZ)],
        [KeyboardButton(text=globals.BTN_LANG_RU)]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(text=globals.TEXT_LANG_WARNING, reply_markup=reply_markup)


async def dec_enter_contact(update, context):
    db_user = db.get_user_by_chat_id(update.message.from_user.id)
    button = [
        [KeyboardButton(
            text=globals.BTN_SEND_CONTACT[db_user["lang_id"]], request_contact=True
        )]
    ]
    reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        text=globals.TEXT_ENTER_CONTACT_WARNING[db_user["lang_id"]],
        reply_markup=reply_markup
    )



