from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals
from buttons import number_to_emoji
from fastfood_db import Database

db = Database()


async def view_cart(context, chat_id, lang_id, user_items, message_id):
    if user_items:
        cart_text = f"<b>🛒 **{globals.AT_KORZINKA[lang_id]}** 🛒</b> \n\n"
        total_price = 0

        for index, item in enumerate(user_items, start=1):
            # Raqamni emoji shaklida olish
            number_emoji = number_to_emoji(index)

            item_name = item['name_uz'] if lang_id == 1 else item['name_ru']
            item_price = item['price']
            item_quantity = item['quantity']

            total_item_price = item_price * item_quantity
            total_price += item_quantity * item_price


            # Mahsulotni tartib raqami bilan qo'shish
            cart_text += (
                f"{number_emoji} <b>**{item_name}**</b>\n"
                f"   ▫️ <b>{globals.QUANTITY[lang_id]}:</b> {item_quantity} \n"
                f"   ▫️ <b>{globals.TEXT_PRODUCT_PRICE[lang_id]}</b> {item_price:,} {globals.SUM[lang_id]}\n"
                f"   ▫️ <b>{globals.ALL[lang_id]}:</b> {total_item_price:,} {globals.SUM[lang_id]}\n\n"
            )

        cart_text += f"<b>🧾 {globals.TOTAL_COST[lang_id]} {total_price:,} {globals.SUM[lang_id]}</b>"

        context.user_data['total_price'] = total_price
        print(context.user_data['total_price'])

        buttons = [
            [InlineKeyboardButton(text=globals.ORDER[lang_id], callback_data='order')],
            [InlineKeyboardButton(text=globals.CLEAR_CART[lang_id], callback_data='clear_cart')],
            [InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        if message_id:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            await context.bot.send_message(chat_id=chat_id,
                                           text=cart_text,
                                           reply_markup=reply_markup,
                                           parse_mode="HTML")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=cart_text,
                                           reply_markup=reply_markup,
                                           parse_mode="HTML")


    else:
        button = [[InlineKeyboardButton(text=globals.BACK[lang_id], callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=button)

        if message_id:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"<b>{globals.EMPTY[lang_id]}</b>",
                                           reply_markup=reply_markup,
                                           parse_mode="HTML")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"<b>{globals.EMPTY[lang_id]}</b>",
                                           reply_markup=reply_markup,
                                           parse_mode="HTML")
