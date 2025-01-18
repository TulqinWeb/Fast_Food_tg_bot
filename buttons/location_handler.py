from telegram import ReplyKeyboardRemove
from fastfood_db import Database
db = Database()
from admin import send_admin_message
import globals

async def location_handler(update, context):
    chat_id = update.message.from_user.id
    user_location = update.message.location
    db_user = db.get_user_by_chat_id(chat_id=chat_id)
    lang_id = db_user['lang_id']

    if user_location:
        latitude = user_location.latitude
        longitude = user_location.longitude

        context.user_data['latitude'] = latitude
        context.user_data['longitude'] = longitude

        await context.bot.send_message(chat_id=chat_id, text=globals.ADDRESS[lang_id],
                                       reply_markup=ReplyKeyboardRemove(),
                                       parse_mode="HTML")

        await send_admin_message(context=context, latitude=latitude,longitude=longitude)

    else:
        print("xatolik")
