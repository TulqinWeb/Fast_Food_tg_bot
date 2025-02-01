import globals
from fastfood_db import Database
db = Database()
from config import ADMIN

async def admin_message_handler(update, context, user_chat_id, user_message_id, admin_message):
    lang_id = db.get_user_by_chat_id(ADMIN)['lang_id']

    if user_chat_id and user_message_id:

        try:
            # Foydalanuvchiga javob yuborish
            await context.bot.send_message(
                chat_id=user_chat_id,
                text=f"Admin javobi:\n\n{admin_message}",
                reply_to_message_id=user_message_id
            )
            # Adminga tasdiq xabarini yuborish
            await update.message.reply_text(text=globals.ADMIN_CONFIRM_MESSAGE[lang_id])
        except Exception as e:
            # Agar xatolik yuzaga kelsa, adminga xabar berish
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")
        finally:
            # Rejimni o'chirish
            context.user_data['reply_user_id'] = None
            context.user_data['reply_message_id'] = None
            context.user_data['admin_awaiting_feedback'] = False
    else:
        await update.message.reply_text("Javob berish uchun tugmani bosing!")
