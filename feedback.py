from aiogram import types
import logging as log
from config import FEEDBACK_USER_ID
from connection import bot, database


async def feedback_message(message: types.Message):
    log.info(f"Message ({message.content_type}) from {message.from_user.first_name} ({message.from_user.id}) with text: {message.text}")

    try:
        if message.from_user.id == FEEDBACK_USER_ID:
            if message.reply_to_message is None:
                await message.answer(f"To reply to the user, reply to the message sent from him")
            else:
                database.execute(
                    '''
                    SELECT user_id 
                    FROM messages 
                    WHERE message_id = ?
                    ''',
                    (message.reply_to_message.message_id,)
                )
                units = database.fetchall()
                unit = units[0][0]
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
                    await bot.send_contact(unit, message.contact.phone_number, "phone_number")
        else:
            forward_message_result = await bot.forward_message(FEEDBACK_USER_ID, message.chat.id, message.message_id)
            database.execute(
                '''
                INSERT OR IGNORE INTO messages(
                user_id,
                first_name,
                message_id,message)
                VALUES(?,?,?,?)
                ''',
                (message.from_user.id,
                 message.from_user.first_name,
                 forward_message_result.message_id,)
            )
    except Exception as e:
        log.exception(e)
