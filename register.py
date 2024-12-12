from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import globals

from fastfood_db import Database

db = Database()


async def check(update, context):
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(chat_id=user.id)

    if not db_user:
        db.create_user(user.id)

        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ)],
            [KeyboardButton(text=globals.BTN_LANG_RU)]
        ]

        update.message.reply_text(text=globals.WELCOME_TEXT)
        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

        context.user_data['satate'] = globals.STATES['reg']


    elif not db_user['lang_id']:
        buttons = [
            [KeyboardButton(text=globals.BTN_LANG_UZ)],
            [KeyboardButton(text=globals.BTN_LANG_RU)]
        ]

        update.message.reply_text(
            text=globals.CHOOSE_LANG,
            reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        )

        context.user_data['state'] = globals.STATES['reg']


    elif not db_user['first_name']:
        update.message.reply_text(text=globals.TEXT_ENTER_FIRST_NAME[db_user['lang_id']],
                                  reply_markup=ReplyKeyboardRemove()
                                  )
        context.user_data['state'] = globals.STATES['reg']


    elif not db_user['last_name']:
        update.message.reply_text(text=globals.TEXT_ENTER_LAST_NAME[db_user['lang_id']],
                                  reply_markup=ReplyKeyboardRemove()
                                  )


    elif not db_user['phone_number']:
        button = [
            [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
        ]

        update.message.reply_text(
            text=globals.TEXT_ENTER_CONTACT[db_user['lang_id']],
            reply_markup=ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        )
        context.user_data['state'] = globals.STATES['reg']

    else:
        pass





