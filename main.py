from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

from buttons import main_menu
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

from config import BOT_TOKEN  # telegram bot token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    if not db_user:
        await start_conv(update, context)
    else:
        await main_menu(update=update,context=context, chat_id=user.id, lang_id=db_user["lang_id"], message_id=None)


def cov_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('start', start_conv)],
        states={
            CHOOSE_LANG: [MessageHandler(filters.TEXT, choose_lang)],
            FIRST_NAME: [MessageHandler(filters.TEXT, enter_first_name)],
            LAST_NAME: [MessageHandler(filters.TEXT, enter_last_name)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.CONTACT, enter_contact)]
        },
        fallbacks=[CommandHandler('cancel', fallbacks)]
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(cov_handler())
    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    app.run_polling()


if __name__ == '__main__':
    main()
