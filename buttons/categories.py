from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals
from fastfood_db import Database

db = Database()


async def all_categories(context, chat_id, lang_id, categories, message_id):
    button = []
    for category in categories:
        button.append(
            [InlineKeyboardButton(
                text=f"{category['name']}",
                callback_data="category_product"
            )]
        )

    button.append([InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back')])
    reply_markup = InlineKeyboardMarkup(inline_keyboard=button)

    if message_id:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=globals.TEXT_ORDER[lang_id],
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text= globals.TEXT_ORDER[lang_id],
            reply_markup=reply_markup
        )