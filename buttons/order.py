from buttons import number_to_emoji
from fastfood_db import Database
db = Database()

import globals

async def order(context, chat_id,user_id,order_id, lang_id,message_id):
    if order_id:
        print(f"Order id {order_id}")
        db.update_order_products(order_id,user_id)
        print("Order qabul qilindi")
        order_list = db.get_last_order(user_id)
        print(order_list)

        order_text = f"{globals.ACCEPT[lang_id]}\n\n"

        order_text +=(
            f"{globals.ORDER_NUMBER[lang_id]} {order_list['id']}\n"
            f"{globals.ORDER_TOTAL_COST} {order_list['total_cost']}\n"
            f"{globals.ORDER_TIME[lang_id]} {order_list['created_at']}")

        for index, product in enumerate(order_list):
            number_emoji = number_to_emoji(index)
            order_text +=(f"{number_emoji}")










