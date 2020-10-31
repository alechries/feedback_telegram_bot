from aiogram import Bot, Dispatcher
import sqlite3 as sql
from config import TELEGRAM_TOKEN, DATABASE_PATH

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)


def database_try_create():
    database_query('''CREATE TABLE IF NOT EXISTS messages(
        user_id INTEGER,
        first_name VARCHAR,
        message_id INT,
        message VARCHAR)''')

    
def database_query(query: str):
    try:
        connect = sql.connect(DATABASE_PATH, check_same_thread=False)
        cursor = connect.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if query.lstrip().upper().startswith("SELECT"):
            connect.commit()
    except sql.Error as e:
        log.error(query, exc_info=e.args[0])
    finally:
        if connect is not None:
            connect.close()
    return result
