
import os

from pyrogram import Client


from command import Locale , fox_command, fox_sudo, who_message


en_strings = {
        "chat_id": "<emoji id='5974526806995242353'>🆔</emoji> Chat ID: `{chat_id}`",
        "user_and_chat": "<emoji id='5974526806995242353'>🆔</emoji> User ID: `{user_id}`\n<emoji id='5974526806995242353'>🆔</emoji> Chat ID: `{chat_id}`"
    }
ru_strings =  {
        "chat_id": "<emoji id='5974526806995242353'>🆔</emoji> ID чата: `{chat_id}`",
        "user_and_chat": "<emoji id='5974526806995242353'>🆔</emoji> ID пользователя: `{user_id}`\n<emoji id='5974526806995242353'>🆔</emoji> ID чата: `{chat_id}`"
    }
ua_strings =  {
        "chat_id": "<emoji id='5974526806995242353'>🆔</emoji> ID чату: `{chat_id}`",
        "user_and_chat": "<emoji id='5974526806995242353'>🆔</emoji> ID користувача: `{user_id}`\n<emoji id='5974526806995242353'>🆔</emoji> ID чату: `{chat_id}`"
    }

locale = Locale(en=en_strings, ru=ru_strings, ua=ua_strings)

@Client.on_message(fox_command("id", "FindIDThisChat", os.path.basename(__file__)) & fox_sudo())
async def find_id(client, message):
    message = await who_message(client, message)
    if message.reply_to_message is None:
        text = locale.get_text("find_id", "chat_id",chat_id=message.chat.id)
        await message.edit(text)
    else:
        text = locale.get_text("find_id", "user_and_chat", LANGUAGES=LANGUAGES, 
                       user_id=message.reply_to_message.from_user.id, 
                       chat_id=message.chat.id)
        await message.edit(text)