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
