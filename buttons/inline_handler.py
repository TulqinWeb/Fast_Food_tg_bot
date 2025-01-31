from buttons import main_menu, all_categories
from buttons.add_to_cart import add_to_cart
from buttons.order import order
from buttons.product_inf import product_inf
from buttons.products import all_products
from buttons.view_cart import view_cart
from fastfood_db import Database
import globals

db = Database()


async def inline_handler(update, context):
    query = update.callback_query
    user = update.callback_query.from_user
    context.user_data['user_chat_id'] = user.id
    db_user = db.get_user_by_chat_id(user.id)

    if query.data == 'main_back':
        # Xabarni "⏱" belgisi bilan tahrirlash
        await query.message.edit_text(
            text='⏳',
            reply_markup=None
        )

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
            context.user_data['selected_category_id'] = category_id

            image_name = db.get_category_image(category_id)
            image_path = f'images/{image_name}'
            products = db.get_products_by_category(category_id)
            await all_products(context=context, chat_id=user.id,
                               lang_id=db_user['lang_id'],
                               products=products,
                               image_path=image_path,
                               message_id=query.message.message_id)


    elif query.data == 'back_category':
        await context.bot.delete_message(chat_id=user.id, message_id=query.message.message_id)

        categories = db.get_categories()
        await all_categories(context=context, chat_id=user.id,
                             lang_id=db_user['lang_id'],
                             categories=categories,
                             message_id=None)

    elif query.data.startswith('product'):
        data_sp = query.data.split('_')
        if data_sp[0] == 'product':
            product_id = int(data_sp[1])
            product = db.get_product(product_id)
            image_name = product['image_url']
            image_path = f'images/{image_name}'
            await product_inf(context=context, chat_id=user.id,
                              lang_id=db_user['lang_id'],
                              product=product, image_path=image_path,
                              message_id=query.message.message_id)

    elif query.data == 'back_products':
        category_id = context.user_data.get('selected_category_id')
        image_name = db.get_category_image(category_id)
        print(image_name)
        image_path = f'images/{image_name}'
        products = db.get_products_by_category(category_id)
        await all_products(context=context, chat_id=user.id,
                           lang_id=db_user['lang_id'],
                           products=products,
                           image_path=image_path,
                           message_id=query.message.message_id)

    elif query.data.startswith("add_to_cart"):
        await add_to_cart(update=update, context=context)

    elif query.data == 'view_cart':
        chat_id = user.id
        db_user = db.get_user_by_chat_id(user.id)
        user_id = db_user['id']
        lang_id = db_user['lang_id']
        user_items = db.get_cart_products(user_id)
        context.user_data['user_items'] = user_items
        await view_cart(context=context, chat_id=chat_id,
                        lang_id=lang_id, user_items=user_items,
                        message_id=query.message.message_id)

    elif query.data == "order":
        total_price = context.user_data.get('total_price')
        print(total_price)
        chat_id = user.id
        user_id = db_user['id']
        lang_id = db_user['lang_id']
        db.order(user_id=user_id, total_price=total_price)
        order_id = db.get_last_order(user_id)['id']
        user_items = db.get_cart_products(user_id)
        await order(context=context, chat_id=chat_id, user_id=user_id,
                    order_id=order_id, user_items=user_items, lang_id=lang_id,
                    message_id=query.message.message_id)

    elif query.data == "clear_cart":
        user_id = db_user['id']
        lang_id = db_user['lang_id']
        db.delete_cart_products(user_id)
        categories = db.get_categories()
        await query.answer(text=f"{globals.CLEAR_CART_ITEMS[lang_id]}", show_alert=False)
        await all_categories(context=context, chat_id=user.id,
                             lang_id=db_user['lang_id'],
                             categories=categories,
                             message_id=query.message.message_id)

    elif query.data == 'back':
        categories = db.get_categories()
        await all_categories(context=context, chat_id=user.id,
                             lang_id=db_user['lang_id'],
                             categories=categories,
                             message_id=query.message.message_id)

    elif query.data.startswith('reply:'):
        data_sp = query.data.split(':')
        user_message_id = data_sp[2].strip()

        # user_chat_id va user_message_id ni int ga o'zgartirish
        try:
            user_message_id = int(user_message_id)
        except ValueError as e:
            await query.message.reply_text(f"Xatolik: {e}")
            return

        context.user_data['reply_message_id'] = user_message_id

        await query.message.reply_text('Foydalanuvchiga javob yozing:')
        context.user_data['admin_awaiting_feedback'] = True
