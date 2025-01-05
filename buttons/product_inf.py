from textwrap import dedent

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals

async def product_inf(context, chat_id, lang_id, product, image_path, message_id):
    default = 1

    inf = dedent(f"""
       {globals.MAHSULOT[lang_id]}: {product['name_uz'] if lang_id == 1 else product['name_ru']}
       {globals.TEXT_PRODUCT_DESC[lang_id]} {product['description_uz'] if lang_id == 1 else product['description_ru']}
       {globals.TEXT_PRODUCT_PRICE[lang_id]} {product['price']} {globals.SUM[lang_id]}
    """).strip()

    buttons = [
        [
            InlineKeyboardButton(text='-', callback_data='decrease'),
            InlineKeyboardButton(text=str(default), callback_data='quantity'),
            InlineKeyboardButton(text='+', callback_data='increase')
        ],
        [
            InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data='add_to_cart')
        ],
        [
            InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back_products')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    if message_id:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

        with open(image_path.strip(), 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=inf,
                reply_markup=reply_markup
            )
    else:
        with open(image_path.strip(), 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=inf,
                reply_markup=reply_markup
            )



