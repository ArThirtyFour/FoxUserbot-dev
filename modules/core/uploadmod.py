# -*- coding: utf-8 -*-
import os

from pyrogram import Client

from command import Locale, fox_command, fox_sudo, who_message
from modules.core.settings.main_settings import file_list

filename = os.path.basename(__file__)
Module_Name = 'Uploadmod'

en_strings = {
    "caption": "<emoji id='5283051451889756068'>🦊</emoji> Module `{module_name}`\nfor FoxUserbot <emoji id='5283051451889756068'>🦊</emoji>\n<b>You can install the module by replying [prefix]loadmod</b>",
    "error": "<emoji id='5210952531676504517'>❌</emoji> **An error has occurred.**\nLog: {error}"
}
ru_strings = {
    "caption": "<emoji id='5283051451889756068'>🦊</emoji> Модуль `{module_name}`\nдля FoxUserbot <emoji id='5283051451889756068'>🦊</emoji>\n<b>Вы можете установить модуль ответом [prefix]loadmod</b>",
    "error": "<emoji id='5210952531676504517'>❌</emoji> **Произошла ошибка.**\nЛог: {error}"
}
ua_strings = {
    "caption": "<emoji id='5283051451889756068'>🦊</emoji> Модуль `{module_name}`\nдля FoxUserbot <emoji id='5283051451889756068'>🦊</emoji>\n<b>Ви можете встановити модуль відповіддю [prefix]loadmod</b>",
    "error": "<emoji id='5210952531676504517'>❌</emoji> **Сталася помилка.**\nЛог: {error}"
}

locale = Locale(en=en_strings, ru=ru_strings, ua=ua_strings)


@Client.on_message(fox_command("uploadmod", Module_Name, filename, "[module name]") & fox_sudo())
async def uploadmod(client, message):
    message = await who_message(client, message)
    try:
        from command import my_prefix
        module_name = message.text.replace(f'{my_prefix()}uploadmod', '')
        params = module_name.split()
        module_name = params[0]
        file = file_list[module_name]
        
        await client.send_document(
            message.chat.id,
            f"modules/loaded/{file}",
            caption=locale.get_text("uploadmod", "caption", module_name=module_name),
            message_thread_id=message.message_thread_id
        )
        await message.delete()
    except Exception as error:

        await message.edit(locale.get_text("uploadmod", "error", error=str(error)))
