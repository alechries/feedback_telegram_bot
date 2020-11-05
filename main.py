from aiogram import types, executor
import logging as log
from feedback import feedback_message
from connection import dispatcher, database


def database_try_create():
    database.execute(
        '''
        CREATE TABLE 
        IF NOT EXISTS messages(
        user_id INTEGER,
        first_name VARCHAR,
        message_id INT,
        message VARCHAR)
        '''
    )


@dispatcher.message_handler(commands=["start"])
async def welcome_message_event(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!")

    
@dispatcher.message_handler(content_types=types.ContentType.ANY)
async def feedback_message_event(message: types.Message):
    await feedback_message(message)


if __name__ == '__main__':
    log.info("Bot started")
    database_try_create()
    executor.start_polling(dispatcher)
