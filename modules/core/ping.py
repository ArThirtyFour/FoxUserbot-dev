# -*- coding: utf-8 -*-
import os
from time import perf_counter
from pyrogram import Client
from command import Locale, fox_command, fox_sudo, who_message

filename = os.path.basename(__file__)
Module_Name = 'Ping'

en_strings = {
    "connect_stable": """<emoji id='5416081784641168838'>🟢</emoji> Stable""",
    "connect_good": "🟠 Good",
    "connect_unstable": """<emoji id='5411225014148014586'>🔴</emoji> Unstable""", 
    "connect_bad": "⚠ Check your network connection",
    "text_return": """<b><emoji id='5269563867305879894'>🏓</emoji> Pong\n<emoji id='5783105032350076195'>📶</emoji></b> {ping} ms\n{connect}"""
}
ru_strings = {
    "connect_stable": """<emoji id='5416081784641168838'>🟢</emoji> Стабильно""",
    "connect_good": "🟠 Терпимо",
    "connect_unstable": """<emoji id='5411225014148014586'>🔴</emoji> Нестабильно""",
    "connect_bad": "⚠ Проверьте подключение", 
    "text_return": """<b><emoji id='5269563867305879894'>🏓</emoji> Понг \n<emoji id='5783105032350076195'>📶</emoji></b> {ping} мс\n{connect}"""
}
ua_strings = {
    "connect_stable": "<emoji id='5416081784641168838'>🟢</emoji> Стабільне",
    "connect_good": "🟠 Піде",
    "connect_unstable": "<emoji id='5411225014148014586'>🔴</emoji> Нестабільне",
    "connect_bad": "⚠️ Перевірте підключення", 
    "text_return": "<emoji id='5269563867305879894'>🏓</emoji> Понг\n<emoji id='5874986954180791957'>📶</emoji> {ping} мс\n{connect}"
}

locale = Locale(en=en_strings, ru=ru_strings, ua=ua_strings)


@Client.on_message(fox_command("ping", Module_Name, filename) & fox_sudo())
async def ping(client, message):
    message = await who_message(client, message)
    
    start = perf_counter()
    await message.edit("🏓| ⚾️=== |🏓")
    await message.edit("🏓| =⚾️== |🏓")
    await message.edit("🏓| ==⚾️= |🏓") 
    await message.edit("🏓| ===⚾️ |🏓")
    end = perf_counter()
    
    ping_time = ((end - start) / 4) * 1000

    if ping_time <= 199:
        connect_key = "connect_stable"
    elif ping_time <= 400:
        connect_key = "connect_good" 
    elif ping_time <= 600:
        connect_key = "connect_unstable"
    else:
        connect_key = "connect_bad"

    connect_text = locale.get_text("ping", connect_key)
    result_text = locale.get_text("ping", "text_return", ping=round(ping_time), connect=connect_text)

    await message.edit(result_text)



