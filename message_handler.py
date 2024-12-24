from buttons import main_menu
from fastfood_db import Database
import globals

db = Database()


async def message_handler(update, context):
    missing_field = context.user_data.get("missing_field")
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)

    if missing_field == "first_name":
        db.update_user_data(user.id, "first_name", update.message.text)
        context.user_data.pop("missing_field")
        return await main_menu(update=update, context=context, chat_id=user.id, lang_id=db_user["lang_id"])

    if missing_field == "last_name":
        db.update_user_data(user.id, "last_name", update.message.text)
        context.user_data.pop("missing_field")
        return await main_menu(update=update, context=context, chat_id=user.id, lang_id=db_user["lang_id"])

    if missing_field == "phone_number":
        contact = update.message.contact
        if contact and contact.phone_number:
            print(contact.phone_number)
            db.update_user_data(user.id, "phone_number", contact.phone_number)
            context.user_data.pop("missing_field")
            return await main_menu(update=update, context=context, chat_id=user.id, lang_id=db_user["lang_id"])

        # Agar kontakt noto'g'ri bo'lsa
        db_user = db.get_user_by_chat_id(user.id)
        await update.message.reply_text(
            text=globals.TEXT_ENTER_CONTACT_WARNING[db_user["lang_id"]]
        )
