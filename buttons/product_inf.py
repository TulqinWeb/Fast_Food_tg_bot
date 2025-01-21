from textwrap import dedent

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals


async def product_inf(context, chat_id, lang_id, product, image_path, message_id):
    current_quantity = 1
    context.user_data['product_id'] = product['id']
    context.user_data[f'quantity_{product['id']}'] = current_quantity

    inf = dedent(f"""
       {globals.MAHSULOT[lang_id]}: {product['name_uz'] if lang_id == 1 else product['name_ru']}
       {globals.TEXT_PRODUCT_DESC[lang_id]} {product['description_uz'] if lang_id == 1 else product['description_ru']}
       {globals.TEXT_PRODUCT_PRICE[lang_id]} {product['price']} {globals.SUM[lang_id]}
    """).strip()

    buttons = [
        [
            InlineKeyboardButton(text='-', callback_data=f'decrease'),
            InlineKeyboardButton(text=str(current_quantity), callback_data='quantity'),
            InlineKeyboardButton(text='+', callback_data=f'increase')
        ],
        [
            InlineKeyboardButton(text=globals.BTN_KORZINKA[lang_id], callback_data=f"add_to_cart_{product['id']}")
        ],
        [
            InlineKeyboardButton(text=globals.SAVAT[lang_id], callback_data='view_cart')
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
