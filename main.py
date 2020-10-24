from aiogram import executor, types
import logging as log

from config import FEEDBACK_USER_ID
from connection import dispatcher, bot, sqlConnect, sqlCursor


@dispatcher.callback_query_handler(lambda query: query.data == "callback")
async def callback_answer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(
        callback_query.id,
        text=callback_query.message.from_user.first_name,
        show_alert=True
    )


@dispatcher.message_handler(lambda message: True, content_types=['text', 'photo', 'sticker', 'video', 'audio', 'voice', 'location', 'animation', 'contact', 'document'])
async def feedback_message(message: types.Message):
    log.info(f'{message.content_type} from {message.from_user.first_name}({message.from_user.id})')

    try:
        if message.from_user.id == FEEDBACK_USER_ID:
            if message.reply_to_message is None:
                await message.answer(f'To reply to the user, reply to the message sent from him')
            else:
                sqlCursor.execute("SELECT user_id FROM USERS WHERE message_id = ?",
                                  (message.reply_to_message.message_id,))

                unit = sqlCursor.fetchall()[0][0]
                if message.content_type == "text":
                    await bot.send_message(unit, message.text)
                elif message.content_type == "photo":
                    await bot.send_photo(unit, message.photo[-1].file_id)
                elif message.content_type == "video":
                    await bot.send_video(unit, message.video.file_id)
                elif message.content_type == "sticker":
                    await bot.send_sticker(unit, message.sticker.file_id)
                elif message.content_type == "audio":
                    await bot.send_audio(unit, message.audio.file_id)
                elif message.content_type == "voice":
                    await bot.send_voice(unit, message.voice.file_id)
                elif message.content_type == "document":
                    await bot.send_document(unit, message.document.file_id)
                elif message.content_type == "location":
                    await bot.send_location(unit, message.location)
                elif message.content_type == "animation":
                    await bot.send_animation(unit, message.animation.file_id)
                elif message.content_type == "contact":
                    await bot.send_contact(unit, message.contact.phone_number)
        else:
            forward_message_result = await bot.forward_message(FEEDBACK_USER_ID, message.chat.id, message.message_id)
            sqlConnect.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",
                               (message.from_user.id, message.from_user.first_name, forward_message_result.message_id,
                                message.text))
    except Exception as e:
        log.exception(e)
    finally:
        sqlConnect.commit()


@dispatcher.message_handler(commands=['start'])
async def welcome_message(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!")


if __name__ == '__main__':
    log.info("Bot started")
    executor.start_polling(dispatcher)
