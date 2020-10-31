import asyncio
from aiogram import types
import logging as log
from feedback import feedback_message
from connection import dispatcher, database_try_create


async def main():
    log.info("Bot started")
    database_try_create()
    await dispatcher.start_polling()


@dispatcher.message_handler(commands=['start'])
async def welcome_message_event(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!")

    
@dp.message_handler(content_types=types.ContentType.ANY)
async def feedback_message_event(message: types.Message):
    await feedback_message(message)


if __name__ == '__main__':
    asyncio.run(main())
