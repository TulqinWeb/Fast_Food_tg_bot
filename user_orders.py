from fastfood_db import Database
db = Database()

async def show_user_orders(update, context, lang_id):
    print(lang_id)
    user_id = update.message.chat_id
    db_user = db.get_user_by_chat_id(user_id)
    orders = db.get_user_orders(db_user['id'], limit=5,lang_id=lang_id)  # Oxirgi 5 ta buyurtma

    if orders:  # Agar buyurtmalar mavjud bo'lsa
        response = "📝 Sizning oxirgi buyurtmalaringiz:\n\n"
        for order in orders:
            products = "\n".join([f"• {product['name']} (x{product['quantity']})" for product in order['products']])
            response += (f"📦 Buyurtma #{order['id']}:\n"
                         f"🗓 Sana: {order['date']}\n"
                         f"💵 Narx: {order['price']} so'm\n"
                         f"🍔 Mahsulotlar:\n{products}\n\n")
        await context.bot.send_message(chat_id=user_id, text=response)
    else:  # Agar buyurtmalar yo'q bo'lsa
        await context.bot.send_message(chat_id=user_id, text="🚫 Sizda hali buyurtma mavjud emas.")