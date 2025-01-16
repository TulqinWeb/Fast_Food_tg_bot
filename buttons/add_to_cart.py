from fastfood_db import Database
db = Database()

import globals

async def add_to_cart(update, context):
    user = update.callback_query.from_user
    db_user = db.get_user_by_chat_id(user.id)
    lang_id = db_user['lang_id']
    user_id = db_user['id']
    query = update.callback_query
    data_sp = query.data.split('_')
    product_id =data_sp[3]
    quantity = context.user_data.get(f'quantity_{product_id}')
    db.add_to_cart_product(user_id, product_id, quantity)

    await query.answer(text=globals.ADD_PRODUCT[lang_id], show_alert=False)
