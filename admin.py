from buttons import number_to_emoji
from config import ADMIN
import globals
from fastfood_db import Database

db = Database()


async def send_admin_message(context, latitude, longitude):
    user_id = context.user_data.get('user_chat_id')
    user_inf = db.get_user_by_chat_id(user_id)
    admin = db.get_user_by_chat_id(ADMIN)
    lang_id = admin['lang_id']
    db_user_id = context.user_data.get('db_user_id')
    order = db.get_last_order(db_user_id)
    print(order)
    order_list = db.get_order_products(db_user_id, order['id'])
    print(order_list)
    user_items = context.user_data.get('user_items')
    print(user_items)

    order_text = (f"<b>Yangi buyurtma</b>\n\n"
                  f"<b>{globals.ORDER_NUMBER[lang_id]} {order_list['order_id']}</b>\n"
                  f"<b>Buyurtma beruvchi: {user_inf['first_name']} {user_inf['last_name']}</b>\n"
                  f"<b>Buyurtma beruvchi telefon raqami: {user_inf['phone_number']}</b>\n\n")

    order_text += (
        f"<b>{globals.ORDER_TOTAL_COST[lang_id]} {order['total_price']}</b>\n"
        f"<b>{globals.ORDER_TIME[lang_id]} {order['created_at']}</b>\n\n"
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
        f"<b> Buyurtma beruvchi manzili</b>\n"
        f"<b> Google maps</b>\n"
        f"https://www.google.com/maps?q={latitude},{longitude}\n\n"
        f"<b>Yandex maps</b>\n"
        f"https://yandex.com/maps/?ll={longitude},{latitude}&z=15"
    )

    if ADMIN:
        await context.bot.send_message(chat_id=ADMIN,
                                       text=order_text,
                                       parse_mode="HTML")

    else:
        print('xatolik')
