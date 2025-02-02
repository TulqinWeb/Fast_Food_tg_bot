from fastfood_db import Database

db = Database()
import globals


async def show_user_orders(update, context, lang_id):
    user_id = update.message.chat_id
    db_user = db.get_user_by_chat_id(user_id)
    orders = db.get_user_orders(db_user['id'], limit=7, lang_id=lang_id)  # Oxirgi 7 ta buyurtma

    if orders:  # Agar buyurtmalar mavjud bo'lsa
        response = f"<b>{globals.LAST_ORDERS[lang_id]}</b>\n\n"
        for order in orders:
            products = "\n".join([f"• {product['name']} (x{product['quantity']})" for product in order['products']])
            response += (f"<b>{globals.ORDER_NUMBER[lang_id]}</b> {order['id']}:\n"
                         f"<b>{globals.ORDER_TIME[lang_id]}</b> {order['date']}\n"
                         f"<b>💵 {globals.ALL[lang_id]}</b> {order['price']} <b>{globals.SUM[lang_id]}</b>\n"
                         f"<b>{globals.ORDER_CONTENT[lang_id]}</b>\n{products}\n\n")
        await context.bot.send_message(chat_id=user_id, text=response,parse_mode="HTML")
    else:  # Agar buyurtmalar yo'q bo'lsa
        await context.bot.send_message(chat_id=user_id, text=f"<b>{globals.NO_ORDERS[lang_id]}</b>",parse_mode="HTML")
