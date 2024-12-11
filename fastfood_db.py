import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD,DB_HOST, DB_PORT

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            db_name = DB_NAME,
            db_user = DB_USER,
            db_password = DB_PASSWORD,
            db_host = DB_HOST,
            db_port = DB_PORT
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,                 
                telegram_id BIGINT NOT NULL,            
                username VARCHAR(50),                  
                full_name VARCHAR(50),                
                phone_number VARCHAR(20),               
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,    
                price DECIMAL(10, 2) NOT NULL, 
                image_url TEXT                 
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
            CREATE TABLE order_items (
                id SERIAL PRIMARY KEY,
                order_id INT REFERENCES orders(id),  
                product_id INT REFERENCES products(id), 
                quantity INT NOT NULL                
                );
             """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,        
                name VARCHAR(50) NOT NULL,     
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)




