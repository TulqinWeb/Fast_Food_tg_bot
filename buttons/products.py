from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals
from fastfood_db import Database

db = Database()


async def all_products(context, chat_id, lang_id, products, image_path, message_id):
    buttons = []
    row = []
    for i, product in enumerate(products):
        product_name = product['name_uz'].strip() if lang_id == 1 else product['name_ru']

        if len(product_name) > 25:
            buttons.append([InlineKeyboardButton(text=product_name, callback_data=f"product_{product['id']}")])
        else:
            row.append(
                (InlineKeyboardButton(text=product_name, callback_data=f"product_{product['id']}"))
            )

            # Har ikkita tugma qo'shilgandan so'ng yangi qator boshlash
            if len(row) == 2:
                buttons.append(row)
                row = []

    # Qolgan tugmalarni qo'shish
    if row:
        buttons.append(row)

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
        with open(image_path.strip(), 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=globals.PRODUCT[lang_id],
                reply_markup=reply_markup
            )
