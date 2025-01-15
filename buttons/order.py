from telegram import KeyboardButton, ReplyKeyboardMarkup

from buttons import number_to_emoji
from fastfood_db import Database

db = Database()

import globals


async def order(context, chat_id, user_id, order_id, user_items, lang_id, message_id):
    if order_id:
        print(f"Order id {order_id}")
        db.update_order_products(order_id, user_id)
        print("Order qabul qilindi")
        order_list = db.get_last_order(user_id)
        print(order_list)

        order_text = f"<b>{globals.ACCEPT[lang_id]}</b>\n\n"

        order_text += (
            f"<b>{globals.ORDER_NUMBER[lang_id]} {order_list['id']}</b>\n"
            f"<b>{globals.ORDER_TOTAL_COST[lang_id]} {order_list['total_price']}</b>\n"
            f"<b>{globals.ORDER_TIME[lang_id]} {order_list['created_at']}</b>\n\n"
            f"<b>{globals.ORDER_CONTENT[lang_id]}</b>\n\n")

        for index, item in enumerate(user_items, start=1):
            # Raqamni emoji shaklida olish
            number_emoji = number_to_emoji(index)
            item_name = item['name_uz'] if lang_id == 1 else item['name_ru']
            item_price = item['price']
            item_quantity = item['quantity']

            total_item_price = item_price * item_quantity

            # Mahsulotni tartib raqami bilan qo'shish
            order_text += (
                f"{number_emoji} <b>**{item_name}**</b>\n"
                f"   ▫️ <b>{globals.QUANTITY[lang_id]}:</b> {item_quantity} \n"
                f"   ▫️ <b>{globals.TEXT_PRODUCT_PRICE[lang_id]}</b> {item_price:,} {globals.SUM[lang_id]}\n"
                f"   ▫️ <b>{globals.ALL[lang_id]}:</b> {total_item_price:,} {globals.SUM[lang_id]}\n\n"
            )

        order_text += (
            f"\n<b>{globals.ORDER_THANKS[lang_id]}</b>\n\n"
            f"<b>{globals.ORDER_PHONE_TEXT[lang_id]}</b>\n\n"
            f"<b>☎️ +998 (90) 123-45-67</b>")

        button = [[KeyboardButton(text="Send location", request_location=True)]]
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

        if message_id:
            await context.bot.edit_message_text(chat_id=chat_id,
                                                text=order_text,
                                                message_id=message_id,
                                                parse_mode="HTML"
                                                )
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"<b>{globals.GET_LOCATION[lang_id]}</b>",
                                           reply_markup=reply_markup,
                                           parse_mode="HTML")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text=order_text,
                                           parse_mode="HTML")
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"<b>{globals.GET_LOCATION[lang_id]}</b>",
                                           reply_markup=reply_markup,
                                           parse_mode="HTML")
