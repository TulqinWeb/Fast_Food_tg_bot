from buttons import main_menu
from config import ADMIN
from fastfood_db import Database
db = Database()
import globals


async def handle_user_message(update, context):
    admin = db.get_user_by_chat_id(ADMIN)
    admin_lang_id = admin['lang_id']
    chat_id = update.message.from_user.id
    db_user = db.get_user_by_chat_id(chat_id)
    lang_id = db_user['lang_id']
    print(db_user)
    user_message = update.message.text
    print(user_message)

    # Agar foydalanuvchi fikr rejimida bo'lsa
    if context.user_data.get('awaiting_feedback'):
        # Adminga fikrni yuborish
        await context.bot.send_message(
            chat_id=ADMIN,
            text=f"{globals.NEW_COMMENT[admin_lang_id]}\n\n"
                 f"{globals.USER[admin_lang_id]} {db_user['first_name']} {db_user['last_name']}\n"
                 f"{globals.COMMENT[admin_lang_id]} {user_message}"
        )
        # Foydalanuvchiga tasdiq xabarini yuborish
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{globals.COMMENT_MESSAGE[lang_id]}"
        )
        # Rejimni o'chirish
        context.user_data['awaiting_feedback'] = False
        await main_menu(context=context,chat_id=chat_id,lang_id=lang_id)
    else:
        # Agar boshqa maqsadda yozilgan bo'lsa
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{globals.COMMENT_WARNING[lang_id]}"
        )
