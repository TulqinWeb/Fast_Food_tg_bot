import psycopg2

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY, 
                first_name VARCHAR(50), 
                last_name VARCHAR(50),
                phone_number VARCHAR(20),                    
                chat_id BIGINT NOT NULL UNIQUE,  -- chat_id ga UNIQUE qo'shildi
                lang_id INTEGER                                                      
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS suggestions (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,  -- Foydalanuvchining chat_id sini saqlaydi
            message TEXT,
            status INTEGER,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(chat_id)  -- chat_id ga bog'lanadi
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,        
                name_uz VARCHAR(50) NOT NULL,   
                name_ru VARCHAR(50) NOT NULL,
                image_url TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name_uz VARCHAR(255) NOT NULL, 
                name_ru VARCHAR(255) NOT NULL,   
                price DECIMAL(10, 2) NOT NULL, 
                description_uz TEXT NOT NULL,
                description_ru TEXT NOT NULL,
                image_url TEXT,
                category_id INTEGER NOT NULL,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES users(id),
                total_price DECIMAL(10, 2) NOT NULL,        
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
             """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_products (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL REFERENCES users(id),
                order_id INT REFERENCES orders(id),  
                product_id INT NOT NULL REFERENCES products(id), 
                quantity INT NOT NULL,
                created_ad TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
             """)

    # Yangi foydalnuvchilarni bazaga saqlash
    def create_user(self, first_name, last_name, phone_number, lang_id, chat_id):
        self.cursor.execute("""
            INSERT INTO users (first_name, last_name, phone_number,lang_id, chat_id) 
            VALUES ( %s,%s,%s,%s,%s)""", (first_name, last_name, phone_number, lang_id, chat_id,))
        self.conn.commit()

    # foydalanuvchining ma'lumotlarini yangilash
    def update_user_lang(self, chat_id, lang_id):
        self.cursor.execute(f"""
            UPDATE users SET lang_id= %s WHERE chat_id= %s """, (lang_id, chat_id))
        self.conn.commit()

    # Foydalanuvchini chat id orqali ma'lumotlarini olish
    def get_user_by_chat_id(self, chat_id):
        self.cursor.execute("""
            SELECT * from users WHERE chat_id= %s""", (chat_id,))
        user = dict_fetchone(self.cursor)
        return user


    def create_category(self, name):
        self.cursor.execute("""
           INSERT INTO categories (name) VALUES (%s)""", (name,))
        self.conn.commit()

    # Barccha categoriyalarni olish
    def get_categories(self):
        self.cursor.execute("""
            SELECT * from categories
            """)
        all_categories = dict_fetchall(self.cursor)
        return all_categories

    # categoriyaga tegishli rasmni olish
    def get_category_image(self, category_id):
        self.cursor.execute("""
            SELECT image_url FROM categories WHERE id = %s
        """, (category_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None


    def create_product(self, name, price, image_url, category_id):
        self.cursor.execute("""
           INSERT INTO products (name, price, image_url, category_id) VALUES ( %s,%s,%s,%s)""",
                            (name, price, image_url, category_id))
        self.conn.commit()

    # Mahsulotlarni categoriya bo'yicha olish
    def get_products_by_category(self, category_id):
        self.cursor.execute("""
            SELECT * from products WHERE category_id = %s""", (category_id,))
        all_products = dict_fetchall(self.cursor)
        return all_products

    # Mahsulotlarni olish
    def get_product(self, product_id):
        self.cursor.execute("""
            SELECT * from products WHERE id= %s """, (product_id,))
        product = dict_fetchone(self.cursor)
        return product

    # Tanlangan mahsulotlarni vaqtinchalik saqlash
    def add_to_cart_product(self, user_id, product_id, quantity):
        self.cursor.execute('''
            INSERT INTO order_products (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
        ''', (user_id, product_id, quantity))
        self.conn.commit()

    # Savatda vaqtinchalik saqlangan mahsulotlarni o'chirish uchun
    def delete_cart_products(self, user_id):
        self.cursor.execute("""
        DELETE from order_products WHERE user_id= %s and order_id IS NULL
        """, (user_id,))
        self.conn.commit()

     # Savatdagi mavsulotlarni olish
    def get_cart_products(self, user_id):
        self.cursor.execute("""
            SELECT 
                products.name_uz AS name_uz,
                products.name_ru AS name_ru,
                products.price AS price,
                order_products.quantity AS quantity
            FROM 
                order_products
            JOIN 
                products ON order_products.product_id = products.id
            WHERE 
                order_products.user_id = %s AND order_products.order_id IS NULL
        """, (user_id,))
        user_order_products = dict_fetchall(self.cursor)
        return user_order_products

    # buyurtmalarni saqlash uchun
    def order(self, user_id, total_price, status='pending'):
        self.cursor.execute("""
        INSERT INTO orders (user_id, total_price, status) 
        VALUES (%s,%s,%s) RETURNING id""", (user_id, total_price, status))
        self.conn.commit()

    # saqlangan buyurtmalarni user_id orqali olish
    def get_order(self, user_id):
        self.cursor.execute("""
        SELECT * from orders WHERE user_id = %s;
        """,(user_id,))
        order = dict_fetchall(self.cursor)
        return order

    # foydalanuvchining oxirgi buyurtmasini olish
    def get_last_order(self, user_id):
        self.cursor.execute("""
        SELECT * FROM orders WHERE user_id = %s
        ORDER BY created_at DESC LIMIT 1;
        """, (user_id,))
        order = dict_fetchone(self.cursor)  # faqat oxirgi buyurtma qaytadi
        return order

    # order_products jadvaliga buyurtma raqamini qo'shish
    def update_order_products(self, order_id, user_id):
        self.cursor.execute("""
        UPDATE order_products 
        SET order_id= %s 
        WHERE user_id=%s AND order_id IS NULL
        """, (order_id, user_id))
        self.conn.commit()

    # buyurtma qilingan mahsulotlarni olish
    def get_order_products(self, user_id, order_id):
        self.cursor.execute("""
        SELECT * FROM order_products WHERE user_id = %s and order_id = %s
        """,(user_id,order_id))
        user_order_products = dict_fetchone(self.cursor)
        return user_order_products

    def get_user_orders(self, user_id, limit=7,lang_id=1):
        # Tilga qarab ustun nomini tanlash
        product_name_column = "name_uz" if lang_id == 1 else "name_ru"

        query = f"""
            SELECT 
                o.id AS order_id,
                o.total_price,
                o.created_at AS order_date,
                op.product_id,
                p.{product_name_column} AS product_name,
                op.quantity
            FROM 
                orders o
            JOIN 
                order_products op ON o.id = op.order_id
            JOIN 
                products p ON op.product_id = p.id
            WHERE 
                o.user_id = %s
            ORDER BY 
                o.created_at DESC
            LIMIT %s;
        """
        self.cursor.execute(query, (user_id, limit))
        rows = self.cursor.fetchall()

        # Buyurtmalarni guruhlash
        orders = {}
        for row in rows:
            order_id = row[0]  # order_id
            if order_id not in orders:
                orders[order_id] = {
                    'id': order_id,
                    'price': row[1],  # total_price
                    'date': row[2].strftime("%Y-%m-%d %H:%M:%S"),  # order_date
                    'products': []
                }
            orders[order_id]['products'].append({
                'name': row[4],  # product_name (name_uz yoki name_ru)
                'quantity': row[5]  # quantity
            })

        return list(orders.values())

    def cleanup_old_cart_items(self):
        self.cursor.execute("""
            DELETE FROM order_products
            WHERE order_id IS NULL
            AND created_at < NOW() - INTERVAL '3 hours';""")
        self.conn.commit()


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
