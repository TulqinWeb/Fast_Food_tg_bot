import globals
from decorator import main_menu
from fastfood_db import Database

db = Database()


async def message_handler(update, context):
    missing_field = context.user_data.get("missing_field")
    user = update.message.from_user

    if missing_field == "first_name":
        first_name = update.message.text
        db.update_user_data(user.id, "first_name", first_name)
        context.user_data.pop("missing_field")
        return await main_menu(update, context)

    if missing_field == "last_name":
        last_name = update.message.text
        db.update_user_data(user.id, "last_name", last_name)
        context.user_data.pop("missing_field")
        return await main_menu(update, context)

    if missing_field == "phone_number":
        db_user = db.get_user_by_chat_id(update.message.from_user.id)
        lang_id = db_user["lang_id"]
        contact = update.message.contact
        if contact and contact.phone_number:
            phone_number = contact.phone_number
            db.update_user_data(user.id, "phone_number", phone_number)
            context.user_data.pop("missing_field")
            return await main_menu(update, context)

        else:
            await update.message.reply_text(
                text=globals.TEXT_ENTER_CONTACT_WARNING[lang_id]
            )
            return

