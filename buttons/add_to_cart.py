from fastfood_db import Database
db = Database()

async def add_to_cart(update, context):
    user = update.callback_query.from_user
    db_user = db.get_user_by_chat_id(user.id)
    user_id = db_user['id']
    print(f"id: {user_id}")
    query = update.callback_query
    data_sp = query.data.split('_')
    print(data_sp)
    product_id =data_sp[3]
    print(f"product_id: {product_id}")
    quantity = context.user_data.get(f'quantity_{product_id}')
    print(f"miqdor: {quantity}")
    db.add_to_cart_product(user_id, product_id, quantity)

    await query.answer(text="Savatga mahsulot qo'shildi!", show_alert=False)
