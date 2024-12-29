from buttons.categories import all_categories
from fastfood_db import Database
import globals

db = Database()


async def message_handler(update, context):
    text = update.message.text
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)

    if text == globals.BTN_ORDER[db_user["lang_id"]]:
        categories = db.get_categories()
        lang_id = db_user["lang_id"]
        await all_categories(context=context, chat_id=user.id, lang_id=lang_id, categories=categories,message_id=None)
