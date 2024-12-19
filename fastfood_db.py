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
                chat_id BIGINT NOT NULL, 
                lang_id INTEGER,                                                      
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,        
                name VARCHAR(50) NOT NULL,     
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,    
                price DECIMAL(10, 2) NOT NULL, 
                image_url TEXT,
                category_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),  
                total_price DECIMAL(10, 2),        
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
             """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INT REFERENCES orders(id),  
                product_id INT REFERENCES products(id), 
                quantity INT NOT NULL                
                );
             """)

    def create_user(self,first_name, last_name, phone_number, lang_id, chat_id):
        self.cursor.execute("""
            INSERT INTO users (first_name, last_name, phone_number,lang_id, chat_id) 
            VALUES ( %s,%s,%s,%s,%s, )""", (first_name, last_name,phone_number,lang_id,chat_id,))
        self.conn.commit()

    def update_user_data(self, chat_id, key, value):
        self.cursor.execute(f"""
            UPDATE users SET {key}= %s WHERE chat_id= %s """, (value, chat_id))
        self.conn.commit()

    def get_user_by_chat_id(self, chat_id):
        self.cursor.execute("""
            SELECT * from users WHERE chat_id= %s""", (chat_id,))
        user = dict_fetchone(self.cursor)
        return user

    def create_category(self, name):
        self.cursor.execute("""
           INSERT INTO categories (name) VALUES (%s)""", (name,))
        self.conn.commit()

    def create_product(self, name, price, image_url, category_id):
        self.cursor.execute("""
           INSERT INTO products (name, price, image_url, category_id) VALUES ( %s,%s,%s,%s)""",
                            (name, price, image_url, category_id))
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
