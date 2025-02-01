async def admin_message_handler(update, context, user_chat_id, user_message_id, admin_message):
    if user_chat_id and user_message_id:

        try:
            # Foydalanuvchiga javob yuborish
            await context.bot.send_message(
                chat_id=user_chat_id,
                text=f"Admin javobi:\n\n{admin_message}",
                reply_to_message_id=user_message_id
            )
            # Adminga tasdiq xabarini yuborish
            await update.message.reply_text("Javobingiz foydalanuvchiga yuborildi!")
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
