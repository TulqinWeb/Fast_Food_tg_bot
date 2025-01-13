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

    cart_text = f"<b>🛒 **{globals.AT_KORZINKA[lang_id]}** 🛒</b> \n\n"
    total_price = 0

    for index, item in enumerate(user_items, start=1):
        item_name = item['name_uz'] if lang_id == 1 else item['name_ru']
        item_price = item['price']
        item_quantity = item['quantity']

        total_item_price = item_price * item_quantity
        total_price += item_quantity * item_price

        # Mahsulotni tartib raqami bilan qo'shish
        cart_text += (
            f"{index}️⃣ <b>**{item_name}**</b>\n"
            f"   ▫️ <b>{globals.QUANTITY[lang_id]}:</b> {item_quantity} \n"
            f"   ▫️ <b>{globals.TEXT_PRODUCT_PRICE[lang_id]}</b> {item_price:,} {globals.SUM[lang_id]}\n"
            f"   ▫️ <b>{globals.ALL[lang_id]}:</b> {total_item_price:,} {globals.SUM[lang_id]}\n\n"
        )

    cart_text += f"<b>🧾 {globals.TOTAL_COST[lang_id]} {total_price:,} {globals.SUM[lang_id]}</b>"

    buttons = [
        [InlineKeyboardButton(text=globals.ORDER[lang_id], callback_data='order')],
        [InlineKeyboardButton(text= globals.CLEAR_CART[lang_id], callback_data='clear_cart')],
        [InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
        await context.bot.send_message(chat_id=chat_id,
                                       text=cart_text,
                                       reply_markup=reply_markup,
                                       parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=chat_id,
                                       text=cart_text,
                                       reply_markup=reply_markup,
                                       parse_mode="HTML")










