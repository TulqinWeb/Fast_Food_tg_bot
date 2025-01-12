from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals
from fastfood_db import Database
db = Database()


async def view_cart(context,chat_id,lang_id,user_items,message_id):
    button = [[InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=button)
    if not user_items:
        await context.bot.send_message(chat_id=chat_id,
                                       text="Savatingiz hozircha bo'sh!",
                                       reply_markup=reply_markup)

    cart_text = f"{globals.AT_KORZINKA[lang_id]}\n\n"
    total_price = 0
    for item in user_items:
        item_name = item['name_uz'] if lang_id == 1 else item['name_ru']
        item_price = item['price']
        item_quantity = item['quantity']

        total_price += item_quantity * item_price

        cart_text += f"{item_name} - {item_quantity} dona - {item_quantity * item_price}{globals.SUM[lang_id]}\n\n"
    cart_text += f"{globals.ALL[lang_id]}: {total_price}{globals.SUM[lang_id]} "

    buttons = [
        [InlineKeyboardButton(text=globals.ORDER[lang_id], callback_data='order')],
        [InlineKeyboardButton(text= globals.CLEAR_CART[lang_id], callback_data='clear_cart')],
        [InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
        await context.bot.send_message(chat_id=chat_id, text=cart_text, reply_markup=reply_markup)
    else:
        await context.bot.send_message(text=cart_text, reply_markup=reply_markup)










