from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import globals

from fastfood_db import Database

db = Database()


async def check(update, context):
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(chat_id=user.id)
    print("db_user:", db_user)

    if not db_user:
        db.create_user(user.id)
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ)],
            [KeyboardButton(text=globals.BTN_LANG_RU)]
        ]
        await update.message.reply_text(text=globals.WELCOME_TEXT)
        print("Yangi foydalanuvchi qo'shildi.")
        await update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        )
        context.user_data['state'] = globals.STATES['reg']

    elif db_user['lang_id'] is None:
        print("Lang ID yo'q")
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ)],
            [KeyboardButton(text=globals.BTN_LANG_RU)]
        ]
        await update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        )
        context.user_data['state'] = globals.STATES['reg']

    elif db_user['first_name'] is None:
        print("First name yo'q")
        await update.message.reply_text(
            text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['state'] = globals.STATES['reg']

    elif db_user['last_name'] is None:
        print("Last name yo'q")
        await update.message.reply_text(
            text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['state'] = globals.STATES['reg']

    elif db_user['phone_number'] is None:
        print("Telefon raqami yo'q")
        button = [
            [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
        ]
        await update.message.reply_text(
            text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
            reply_markup=ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        )
        context.user_data['state'] = globals.STATES['reg']

    else:
        await update.message.reply_text("Barcha ma'lumotlar mavjud. Davom eting.")


async def check_data_decorator(func):
    async def inner(update, context):
        user = update.message.from_user
        db_user = db.get_user_by_chat_id(user.id)
        state = context.user_data.get('state', 0)

        if state != globals.STATES['reg']:

            if not db_user:
                db.create_user(user.id)
                buttons = [
                    [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
                ]
                await update.message.reply_text(text=globals.WELCOME_TEXT)
                await update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["lang_id"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_LANG_UZ), KeyboardButton(text=globals.BTN_LANG_RU)]
                ]
                await update.message.reply_text(
                    text=globals.CHOOSE_LANG,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["first_name"]:
                await update.message.reply_text(
                    text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["last_name"]:
                await update.message.reply_text(
                    text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
                    reply_markup=ReplyKeyboardRemove()
                )
                context.user_data["state"] = globals.STATES["reg"]

            elif not db_user["phone_number"]:
                buttons = [
                    [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
                ]
                await update.message.reply_text(
                    text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=buttons,
                        resize_keyboard=True
                    )
                )
                context.user_data["state"] = globals.STATES["reg"]

            else:
                return await func(update, context)
            return False

        else:
            return await func(update, context)

    return inner
