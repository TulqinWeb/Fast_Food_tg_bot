from buttons import main_menu, all_categories
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


    elif query.data.startswith('category'):
        data_sp = query.data.split('_')
        if data_sp[0] == 'category':
            category_id = int(data_sp[1])
            products = db.get_products_by_category(category_id)
            await all_products(context=context, chat_id=user.id,
                           lang_id=db_user['lang_id'],
                           products=products,
                           message_id=query.message.message_id)

    elif query.data.startswith('product'):
        data_sp = query.data.split('_')
        if data_sp[0] == 'product':
            category_id = int(data_sp[1])
            products = db.get_product_in_category(category_id)
            await all_products(context=context, chat_id=user.id,
                           lang_id=db_user['lang_id'],
                           products=products,
                           message_id=query.message.message_id)

    elif query.data == 'back_category':
        categories = db.get_categories()
        await all_categories(context=context, chat_id=user.id,
                             lang_id=db_user['lang_id'],
                             categories=categories,
                             message_id=query.message.message_id)
