from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import globals

async def all_products(context, chat_id, lang_id, products, message_id):
    buttons = []
    for product in products:
        product_name = product['name_uz'] if lang_id == 1 else product['name_ru']
        buttons.append(
            [InlineKeyboardButton(text=product_name, callback_data=f"product_{product['id']}")]
        )

    buttons.append([InlineKeyboardButton(text=globals.BACK[lang_id], callback_data=f"category_back")])
    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    if message_id:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=globals.PRODUCT[lang_id],
            reply_markup=reply_markup
        )

    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=globals.PRODUCT[lang_id],
            reply_markup=reply_markup
        )
