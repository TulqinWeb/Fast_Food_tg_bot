from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from register import check
# Enable logging
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

from config import BOT_TOKEN  # telegram bot token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await check(update,context)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
