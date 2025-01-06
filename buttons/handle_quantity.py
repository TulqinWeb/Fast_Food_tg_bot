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

    # Avvalgi miqdorni olish
    current_quantity = context.user_data.get('quantity', 1)

    if query.data == 'increase':
        current_quantity += 1
    elif query.data == 'decrease':
        if current_quantity > 1:
            current_quantity -= 1
        else:
            await query.answer(globals.NOTICE[lang_id], show_alert=True)


    context.user_data['quantity'] = current_quantity

    buttons = [
        [
            InlineKeyboardButton(text='-', callback_data='decrease'),
            InlineKeyboardButton(text=str(current_quantity), callback_data='quantity'),
            InlineKeyboardButton(text='+', callback_data='increase')
        ],
        [
            InlineKeyboardButton(text=globals.BTN_KORZINKA[lang_id], callback_data='add_to_cart')
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
