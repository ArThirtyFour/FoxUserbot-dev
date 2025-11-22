# -*- coding: utf-8 -*-
import os
import shutil
import traceback
import zipfile

import wget
from pyrogram import Client
from pyrogram.types import Message

from command import Locale, fox_command, fox_sudo, who_message

filename = os.path.basename(__file__)
Module_Name = 'Restarter'

en_strings = {
    "updating": "<emoji id='5264727218734524899'>🔄</emoji> **Updating {repo_type}...**",
    "update_success": "<emoji id='5237699328843200968'>✅</emoji> **Userbot successfully updated\n<emoji id='5264727218734524899'>🔄</emoji> Restarting...**",
    "error_occurred": "<emoji id='5210952531676504517'>❌</emoji> **An error occurred:**\n\n`{error}`",
    "restarting": "<emoji id='5264727218734524899'>🔄</emoji> **Restarting userbot...**",
    "restart_error": "<emoji id='5210952531676504517'>❌</emoji> **An error occurred...**"
}
ru_strings = {
    "updating": "<emoji id='5264727218734524899'>🔄</emoji> **Обновление {repo_type}...**",
    "update_success": "<emoji id='5237699328843200968'>✅</emoji> **Юзербот успешно обновлен\n<emoji id='5264727218734524899'>🔄</emoji> Перезапуск...**",
    "error_occurred": "<emoji id='5210952531676504517'>❌</emoji> **Произошла ошибка:**\n\n`{error}`",
    "restarting": "<emoji id='5264727218734524899'>🔄</emoji> **Перезапуск юзербота...**",
    "restart_error": "<emoji id='5210952531676504517'>❌</emoji> **Произошла ошибка...**"
}
ua_strings = {
    "updating": "<emoji id='5264727218734524899'>🔄</emoji> **Оновлення {repo_type}...**",
    "update_success": "<emoji id='5237699328843200968'>✅</emoji> **Юзербот успішно оновлено\n<emoji id='5264727218734524899'>🔄</emoji> Перезавантаження...**",
    "error_occurred": "<emoji id='5210952531676504517'>❌</emoji> **Сталася помилка:**\n\n`{error}`",
    "restarting": "<emoji id='5264727218734524899'>🔄</emoji> **Перезапуск юзербота...**",
    "restart_error": "<emoji id='5210952531676504517'>❌</emoji> **Сталася помилка...**"
}

locale = Locale(en=en_strings, ru=ru_strings, ua=ua_strings)


def restart_executor(chat_id=None, message_id=None, text=None, thread=None):
    if os.name == "nt":
        os.execvp(
            "python",
            [
                "python",
                "main.py",
                f"{chat_id}",
                f"{message_id}",
                f"{text}",
                f"{thread}" if thread else "None",
            ],
        )
    else:
        os.execvp(
            "python3",
            [
                "python3",
                "main.py",
                f"{chat_id}",
                f"{message_id}",
                f"{text}",
                f"{thread}" if thread else "None",
            ],
        )


async def restart(message: Message, restart_type):
    if restart_type == "update":
        text = "1"
    else:
        text = "2"
    thread_id = message.message_thread_id if message.message_thread_id else None
    chat_id = message.chat.username if message.chat.username else message.chat.id
    restart_executor(chat_id, message.id, text, thread_id)


async def update_repository(client, message, repo_url, repo_type):
    try:
        try:
            os.remove("temp/archive.zip")
        except:
            pass
        
        await message.edit(locale.get_text("restarter", "updating", repo_type=repo_type))

        wget.download(repo_url, 'temp/archive.zip')

        with zipfile.ZipFile("temp/archive.zip", "r") as zip_ref:
            file_list = zip_ref.namelist()
            root_folder = None
            for file in file_list:
                if file.endswith('/') and file.count('/') == 1:
                    root_folder = file.strip('/')
                    break
            
            if not root_folder:
                raise Exception("Not found root dir")

            zip_ref.extractall("temp/")

        os.remove("temp/archive.zip")
        shutil.make_archive("temp/archive", "zip", f"temp/{root_folder}/")
        with zipfile.ZipFile("temp/archive.zip", "r") as zip_ref:
            zip_ref.extractall(".")

        os.remove("temp/archive.zip")
        shutil.rmtree(f"temp/{root_folder}")
        
        await message.edit(locale.get_text("restarter", "update_success"))
        await restart(message, restart_type="update")
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_message = locale.get_text("restarter", "error_occurred", error=str(e))

        if len(error_message) > 4000:
            error_message = error_message[:4000] + "..."
        
        await message.edit(error_message)


# Restart
@Client.on_message(fox_command("restart", Module_Name, filename) & fox_sudo())
async def restart_get(client, message):
    message = await who_message(client, message)
    try:
        await message.edit(locale.get_text("restarter", "restarting"))
        await restart(message, restart_type="restart")
    except:
        await message.edit(locale.get_text("restarter", "restart_error"))


# Update main
@Client.on_message(fox_command("update", Module_Name, filename) & fox_sudo())
async def update(client, message):
    message = await who_message(client, message)
    await update_repository(client, message, "https://github.com/FoxUserbot/FoxUserbot/archive/refs/heads/main.zip", "main")


# Update beta
@Client.on_message(fox_command("beta", Module_Name, filename) & fox_sudo())
async def update_beta(client, message):
    message = await who_message(client, message)

    await update_repository(client, message, "https://github.com/FoxUserbot/FoxUserbot-dev/archive/refs/heads/main.zip", "beta")
