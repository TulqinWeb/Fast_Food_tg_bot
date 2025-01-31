from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler

from admin_message_handler import admin_message_handler
from buttons import location_handler
from buttons.handle_quantity import handle_quantity
from buttons.inline_handler import inline_handler
from comment_handler import handle_user_message
from message_handler import message_handler

from register import start_conv, choose_lang, enter_first_name, enter_last_name, CHOOSE_LANG, FIRST_NAME, LAST_NAME, \
    CONTACT, enter_contact, fallbacks

from fastfood_db import Database

db = Database()

# Enable logging
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

from config import BOT_TOKEN, ADMIN  # telegram bot token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_conv(update, context)


def cov_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('start', start_conv)],
        states={
            CHOOSE_LANG: [MessageHandler(filters.TEXT, choose_lang)],
            FIRST_NAME: [MessageHandler(filters.TEXT, enter_first_name)],
            LAST_NAME: [MessageHandler(filters.TEXT, enter_last_name)],
            CONTACT: [MessageHandler(filters.TEXT | filters.CONTACT, enter_contact)]
        },
        fallbacks=[CommandHandler('cancel', fallbacks)]
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Mavjud handlerlar
    app.add_handler(cov_handler())
    app.add_handler(CallbackQueryHandler(handle_quantity, pattern='^(increase|decrease)$'))
    app.add_handler(CallbackQueryHandler(inline_handler))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))
    # Umumiy message_handler (oxirgi qo'shiladi)
    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    # # Yangi qo'shilgan handlerlar (avval admin va foydalanuvchi handlerlari)
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.User(ADMIN), handle_user_message))   # Foydalanuvchi xabarlari
    # app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN), admin_message_handler))  # Admin xabarlari




    app.run_polling()


if __name__ == '__main__':
    main()

