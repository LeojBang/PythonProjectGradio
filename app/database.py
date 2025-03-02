import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings

# Настройка логирования
logging.basicConfig(filename="logs/app.log", level=logging.ERROR)

def get_db_connection():
    """Возвращает соединение с базой данных."""
    try:
        return psycopg2.connect(
            dbname=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise

def init_db():
    """Создает базу данных и таблицы, если они не существуют."""
    conn = None  # Инициализируем переменную conn
    try:
        # Подключение к базе данных
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Создание таблицы requests, если она не существует
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    model_name TEXT NOT NULL,
                    description TEXT NOT NULL
                );
            """)
            conn.commit()
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise
    finally:
        if conn:  # Проверяем, что conn была инициализирована
            conn.close()

def save_request(model_name, description):
    """Сохраняет запрос в базу данных."""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO requests (model_name, description) VALUES (%s, %s)",
                (model_name, description)
            )
            conn.commit()
    except Exception as e:
        logging.error(f"Error saving request: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_requests():
    """Возвращает историю запросов."""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM requests ORDER BY timestamp DESC")
            return cur.fetchall()
    except Exception as e:
        logging.error(f"Error fetching requests: {e}")
        raise
    finally:
        if conn:
            conn.close()