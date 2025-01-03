from buttons import main_menu
from buttons.products import all_products
from fastfood_db import Database

db = Database()


async def inline_handler(update, context):
    query = update.callback_query
    user = update.callback_query.from_user
    db_user = db.get_user_by_chat_id(user.id)
    print(query.data)

    if query.data == 'main_back':
        await context.bot.delete_message(
            chat_id=user.id,
            message_id=query.message.message_id
        )

        await main_menu(context=context, chat_id=user.id,
                        lang_id=db_user['lang_id'],
                        message_id=None)

    data_sp = query.data.split('_')
    print(data_sp)
    if data_sp[0] == 'category':
        category_id = data_sp[1]
        products = db.get_products_by_category(category_id)
        await all_products(context=context, chat_id=user.id,
                           lang_id=db_user['lang_id'],
                           products=products,
                           message_id=query.message.message_id)

    data_sp = str(query.data.split('_'))
    if data_sp[0] == 'product':
        category_id = int(data_sp[1])
        products = db.get_product_in_category(category_id)
        await all_products(context=context, chat_id=user.id,
                           lang_id=db_user['lang_id'],
                           products=products,
                           message_id=query.message.message_id)

    if query.data == 'category_back':
        categories = db.get_categories()
        for category in categories:
            category_id = category['id']
            products = db.get_products_by_category(category_id)
            await all_products(context=context, chat_id=user.id,
                               lang_id=db_user['lang_id'],
                               products=products,
                               message_id=query.message.message_id)
