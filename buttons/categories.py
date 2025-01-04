from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals
from fastfood_db import Database

db = Database()


async def all_categories(context, chat_id, lang_id, categories, message_id):
    buttons = []
    row = []
    for i, category in enumerate(categories):
        category_name = category['name_uz'].strip() if lang_id == 1 else category['name_ru']

        if len(category_name) > 15:
            buttons.append(
                [InlineKeyboardButton(
                    text=category_name,
                    callback_data=f"category_{category['id']}"
                )]
            )
        else:
            row.append(
                (InlineKeyboardButton(
                    text=category_name,
                    callback_data=f"category_{category['id']}"
                ))
            )

            if len(row) == 2:
                buttons.append(row)
                row = []
    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='main_back')])
    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

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
            text=globals.TEXT_ORDER[lang_id],
            reply_markup=reply_markup
        )
