# -*- coding: utf-8 -*-
import os
import random
from subprocess import PIPE, Popen, TimeoutExpired
from time import perf_counter

from pyrogram import Client

from command import Locale, fox_command, fox_sudo, who_message

filename = os.path.basename(__file__)
Module_Name = 'Shell'

en_strings = {
    "no_command": "<emoji id='5210952531676504517'>❌</emoji> <b>Specify the command in message text or in reply</b>",
    "running": "<emoji id='5264727218734524899'>🔄</emoji> <b>Running...</b>",
    "timeout": "<emoji id='5210952531676504517'>❌</emoji> <b>Timeout expired (60 seconds)</b>",
    "output": "<emoji id='5447410659077661506'>🌐</emoji> <b>Output:</b>",
    "error": "<emoji id='5210952531676504517'>❌</emoji> <b>Error:</b>",
    "completed": "<emoji id='5237699328843200968'>✅</emoji> <b>Completed in {time} miliseconds with code {code}</b>",
    "too_large": "<emoji id='5411225014148014586'>🔴</emoji> <b>Result too much, send with document...</b>"
}
ru_strings = {
    "no_command": "<emoji id='5210952531676504517'>❌</emoji> <b>Укажите команду в тексте сообщения или в ответе</b>",
    "running": "<emoji id='5264727218734524899'>🔄</emoji> <b>Выполнение...</b>",
    "timeout": "<emoji id='5210952531676504517'>❌</emoji> <b>Время ожидания истекло (60 секунд)</b>",
    "output": "<emoji id='5447410659077661506'>🌐</emoji> <b>Вывод:</b>",
    "error": "<emoji id='5210952531676504517'>❌</emoji> <b>Ошибка:</b>",
    "completed": "<emoji id='5237699328843200968'>✅</emoji> <b>Завершено за {time} миллисекунд с кодом {code}</b>",
    "too_large": "<emoji id='5411225014148014586'>🔴</emoji> <b>Результат слишком большой, отправляю файлом...</b>"
}
ua_strings = {
    "no_command": "<emoji id='5210952531676504517'>❌</emoji> <b>Вкажіть команду в тексті повідомлення або у відповіді</b>",
    "running": "<emoji id='5264727218734524899'>🔄</emoji> <b>Виконання...</b>",
    "timeout": "<emoji id='5210952531676504517'>❌</emoji> <b>Час очікування вичерпано (60 секунд)</b>",
    "output": "<emoji id='5447410659077661506'>🌐</emoji> <b>Результат:</b>",
    "error": "<emoji id='5210952531676504517'>❌</emoji> <b>Помилка:</b>",
    "completed": "<emoji id='5237699328843200968'>✅</emoji> <b>Завершено за {time} мілісекунд з кодом {code}</b>",
    "too_large": "<emoji id='5411225014148014586'>🔴</emoji> <b>Результат занадто великий, надсилаю файлом...</b>"
}

locale = Locale(en=en_strings, ru=ru_strings, ua=ua_strings)


@Client.on_message(fox_command(["shell", "sh"], Module_Name, filename, "[command/reply]") & fox_sudo())
async def shell(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message and (len(message.text.split()) == 1):
        return await message.edit(locale.get_text("shell", "no_command"))
    
    cmd_text = (
        " ".join(message.text.split()[1:])
        if message.text and len(message.text.split()) > 1
        else (
            message.reply_to_message.text
            if message.reply_to_message and message.reply_to_message.text
            else None
        )
    )
    if cmd_text is None: 
        cmd_text = " ".join(message.text.split()[1:])
    
    cmd_obj = Popen(cmd_text, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    await message.edit(locale.get_text("shell", "running"))
    
    text = f"$ <code>{cmd_text}</code>\n\n"
    
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += locale.get_text("shell", "timeout")
    else:
        stop_time = perf_counter()
        
        if stdout:
            stdout_output = f"{stdout}"
            text += f"{locale.get_text('shell', 'output')}\n```\n{stdout}\n```\n\n"
        else:
            stdout_output = ""

        if stderr:
            stderr_output = f"{stderr}"
            text += f"{locale.get_text('shell', 'error')}\n```\n{stderr}\n```\n\n"
        else:
            stderr_output = ""

        time = round(stop_time - start_time, 3) * 1000
        text += locale.get_text("shell", "completed", time=time, code=cmd_obj.returncode)

    try:
        await message.edit(text)
    except:
        output = f"{stdout_output}\n\n{stderr_output}"
        command = f"{cmd_text}"

        await message.edit(locale.get_text("shell", "too_large"))

        i = random.randint(1, 9999)
        with open(f"temp/result{i}.txt", "w") as file:
            file.write(f"{output}")

        try:
            await client.send_document(
                message.chat.id, 
                f"temp/result{i}.txt", 
                caption=f"<code>{command}</code>", 
                message_thread_id=message.message_thread_id
            )
            await message.delete()
        except:
            await client.send_document(
                message.chat.id, 
                f"temp/result{i}.txt", 
                caption="Result", 
                message_thread_id=message.message_thread_id
            )
            await message.edit(f"<code>{command}</code>")
        os.remove(f"temp/result{i}.txt")
    

    cmd_obj.kill()
