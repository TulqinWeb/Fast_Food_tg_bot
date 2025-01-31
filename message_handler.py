from telegram import ReplyKeyboardRemove, Message, KeyboardButton, ReplyKeyboardMarkup

from admin_message_handler import admin_message_handler
from buttons.categories import all_categories
from buttons.main_menu import main_menu
from comment_handler import handle_user_message
from fastfood_db import Database
import globals

db = Database()


async def message_handler(update, context):
    text = update.message.text
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    lang_id = db_user['lang_id']
    context.user_data['db_user_id'] = db_user['id']

    # Boshqa xabarlar uchun umumiy handler
    if context.user_data.get('awaiting_feedback'):
        # Fikr kutayotgan bo'lsa, handle_user_messageni chaqiramiz
        await handle_user_message(update, context)

    if text == globals.BTN_ORDER[lang_id]:
        temp_message: Message = await context.bot.send_message(chat_id=user.id,
                                       text=".",
                                       reply_markup = ReplyKeyboardRemove()
        )
        #yuqoridagi yuborilgan xabarni o'chirish uchun
        await context.bot.delete_message(chat_id=user.id,  message_id=temp_message.message_id)

        categories = db.get_categories()
        lang_id = db_user["lang_id"]
        await all_categories(context=context, chat_id=user.id, lang_id=lang_id, categories=categories,message_id=None)

    elif text == globals.BTN_ABOUT_US[lang_id]:
        message = globals.ABOUT_COMPANY[lang_id]
        await context.bot.send_message(chat_id=user.id,text=message,parse_mode="HTML")

    elif text == globals.BTN_SETTINGS[lang_id]:
        button = [
            [KeyboardButton(text=globals.BTN_LANG_UZ)],[KeyboardButton(text=globals.BTN_LANG_RU)]
        ]
        reply_markup = ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

        await context.bot.send_message(chat_id= user.id, text=globals.CHOOSE_LANG, reply_markup=reply_markup)

    elif text == globals.BTN_LANG_UZ:
        lang_id = 1
        db.update_user_lang(chat_id=user.id, lang_id=lang_id)
        await main_menu(context=context,chat_id=user.id,lang_id=lang_id)

    elif text == globals.BTN_LANG_RU:
        lang_id = 2
        db.update_user_lang(chat_id=user.id, lang_id=lang_id)
        await main_menu(context=context, chat_id=user.id, lang_id=lang_id)

    elif text == globals.BTN_COMMENTS[lang_id]:

        await context.bot.send_message(
            chat_id=user.id,
            text=globals.SEND_COMMENT[lang_id],
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data['awaiting_feedback'] = True  # Fikr kutayotgan rejimni belgilash

    elif context.user_data.get('admin_awaiting_feedback'):
        admin_message = update.message.text
        user_chat_id = user.id
        user_message_id = context.user_data.get('reply_message_id')

        await admin_message_handler(update=update,context=context,user_chat_id=user_chat_id,user_message_id=user_message_id,admin_message=admin_message)

    # else:
    #     await context.bot.send_message(chat_id=user.id, text=globals.ELSE[lang_id])





