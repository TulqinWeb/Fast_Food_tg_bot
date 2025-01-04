from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals
from fastfood_db import Database

db = Database()


async def all_products(context, chat_id, lang_id, products,image_path, message_id):
    buttons = []
    for product in products:
        product_name = product['name_uz'] if lang_id == 1 else product['name_ru']
        buttons.append(
            [InlineKeyboardButton(text=product_name, callback_data=f"product_{product['id']}")]
        )

    buttons.append([InlineKeyboardButton(text=globals.BACK[lang_id], callback_data=f"back_category")])
    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=globals.PRODUCT[lang_id],
                reply_markup=reply_markup
            )


    else:
        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=globals.PRODUCT[lang_id],
                reply_markup=reply_markup
            )

