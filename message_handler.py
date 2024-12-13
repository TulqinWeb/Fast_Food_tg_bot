from telegram import KeyboardButton

from check_data_decorator import check_data_decorator
from register import check
from fastfood_db import Database
import globals

db = Database()


@check_data_decorator
async def message_handler(update, context):
    message = update.message.text
    user = update.message.from_user
    state = context.user_data.get('state', 0)
    db_user = db.get_user_by_chat_id(user.id)
    if state == 0:
       print(state)
       await check(update=update, context=context)

    elif state == 1:
        if not db_user['lang_id']:
            if message == globals.BTN_LANG_UZ:
                db.update_user_data(user.id, 'lang_id', 1)
                await check(update, context)

            elif message == globals.BTN_LANG_RU:
                db.update_user_data(user.id, 'lang_id', 2)
                await check(update, check)

            else:
                await update.message.reply_text(text=globals.TEXT_LANG_WARNING)

        elif not db_user['first_name']:
            db.update_user_data(user.id, 'first_name', message)
            await check(update, context)

        elif not db_user['last_name']:
            db.update_user_data(user.id, 'last_name', message)
            button = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
            ]
            await check(update, context)

        elif not db_user['phone_number']:
            db.update_user_data(user.id, 'phone_number', message)

        else:
            await check(update, context)







