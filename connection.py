from aiogram import Bot, Dispatcher
import sqlite3 as sql
from config import TELEGRAM_TOKEN, DATABASE_PATH
import logging as log
import traceback

# Connections at the bottom of the file


class Database:
    def __init__(self, path: str):
        log.info("Starting database initialization")
        try:
            self.__connect = sql.connect(path)
            self.__cursor = self.__connect.cursor()
            log.info("Database initialization was successful")
        except Exception as e:
            log.error("Exc.", exc_info=e)

    def __del__(self):
        log.info("Closing the database")
        self.__connect.commit()
        self.__connect.close()

    def execute(self, query: str, parameters: tuple = None):
        try:
            if not parameters:
                parameters = ()
            self.__cursor.execute(query, parameters)
            if query.lstrip().upper().startswith("SELECT"):
                self.__connect.commit()
        except sql.Error as e:

            log.error(f"!!! FROM {traceback.StackSummary.extract(traceback.walk_stack(None))} !!!" + query, exc_info=e.args[0])

    def fetchone(self):
        try:
            result = self.__cursor.fetchone()
            return result
        except sql.Error as e:
            log.error(e.args[0])

    def fetchall(self):
        try:
            result = self.__cursor.fetchall()
            return result
        except sql.Error as e:
            log.error(e.args[0])

    def fetchmany(self, size: int):
        try:
            result = self.__cursor.fetchmany(size)
            return result
        except sql.Error as e:
            log.error(e.args[0])


bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)
database = Database("chat.db")
