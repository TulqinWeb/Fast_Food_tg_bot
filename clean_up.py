import schedule
import time
from fastfood_db import Database

db = Database()


# order_products jadvaliga vaqtinchalik saqlangan order_id null bo'lib qolgan barcha productlarni o'chiradi
def cleanup_task():
    db.cleanup_old_cart_items()


# Har 1 soatda cleanup_task funksiyasini ishga tushirish
schedule.every(12).hours.do(cleanup_task)

while True:
    schedule.run_pending()
    time.sleep(12)
