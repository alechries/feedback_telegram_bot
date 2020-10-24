from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN, DATABASE_PATH
import sqlite3 as sql

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)

sqlConnect = sql.connect(DATABASE_PATH, check_same_thread=False)
sqlCursor = sqlConnect.cursor()
sqlCursor.execute('''CREATE TABLE IF NOT EXISTS USERS(
    user_id INTEGER,
    first_name VARCHAR,
    message_id INT,
    message VARCHAR)''')