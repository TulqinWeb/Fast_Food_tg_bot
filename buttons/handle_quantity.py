from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals
from fastfood_db import Database

db = Database()


async def handle_quantity(update, context):
    user = update.callback_query.from_user
    db_user = db.get_user_by_chat_id(user.id)
    lang_id = db_user['lang_id']

    query = update.callback_query
    print(query.data)
    product_id = context.user_data.get('product_id')

    # Avvalgi miqdorni olish
    current_quantity = context.user_data.get(f'quantity_{product_id}', 1)
    print(current_quantity)

    if query.data == 'increase':
        current_quantity += 1
        print(current_quantity)
    elif query.data == 'decrease':
        if current_quantity > 1:
            current_quantity -= 1
        else:
            await query.answer(globals.NOTICE[lang_id], show_alert=True)

    context.user_data[f'quantity_{product_id}'] = current_quantity
    print(current_quantity)

    buttons = [
        [
            InlineKeyboardButton(text='-', callback_data='decrease'),
            InlineKeyboardButton(text=str(current_quantity), callback_data='quantity'),
            InlineKeyboardButton(text='+', callback_data='increase')
        ],
        [
            InlineKeyboardButton(text=globals.BTN_KORZINKA[lang_id], callback_data=f'add_to_cart_{product_id}')
        ],
        [
            InlineKeyboardButton(text=globals.SAVAT[lang_id], callback_data='view_cart')
        ],
        [
            InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back_products')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    # Joriy reply_markup bilan solishtirish
    if query.message.reply_markup == reply_markup:
        return

    # Xabarni yangilash
    await query.edit_message_reply_markup(reply_markup=reply_markup)
