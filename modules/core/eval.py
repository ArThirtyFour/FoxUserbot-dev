# -*- coding: utf-8 -*-
import os
import sys
from io import StringIO

from pyrogram import Client

from command import Locale , fox_command, fox_sudo, who_message

strings_en = {
        "success": """<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Code:</b>
<code>{code}</code>

<emoji id='5447410659077661506'>🌐</emoji> <b>Result</b>:
<code>{result}</code>""",
        "error": """<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Code:</b>
<code>{code}</code>

<emoji id='5447410659077661506'>🌐</emoji> <b>Result</b>:
<code>{error_type}: {error_message}</code>"""
    }
strings_ru = {
        "success": """<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Код:</b>
<code>{code}</code>

<emoji id='5447410659077661506'>🌐</emoji> <b>Результат</b>:
<code>{result}</code>""",
        "error": """<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Код:</b>
<code>{code}</code>

<emoji id='5447410659077661506'>🌐</emoji> <b>Результат</b>:
<code>{error_type}: {error_message}</code>"""
    }
strings_ua = {
        "success": """<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Код:</b>
<code>{code}</code>

<emoji id='5447410659077661506'>🌐</emoji> <b>Результат</b>:
<code>{result}</code>""",
        "error": """<emoji id='5300928913956938544'>👩‍💻</emoji> <b>Код:</b>
<code>{code}</code>

<emoji id='5447410659077661506'>🌐</emoji> <b>Результат</b>:
<code>{error_type}: {error_message}</code>"""
    }

locale = Locale(en=strings_en, ru=strings_ru, ua=strings_ua)

@Client.on_message(fox_command("eval", "Eval", os.path.basename(__file__), "[code/reply]") & fox_sudo())
async def user_exec(client, message):
    message = await who_message(client, message)
    reply = message.reply_to_message
    code = ""
    try:
        code = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        try:
            code = message.text.split(" \n", maxsplit=1)[1]
        except IndexError:
            pass

    result = sys.stdout = StringIO()
    try:
        exec(code)
        result_text = locale.get_text("eval", "success", 
                              code=code, result=result.getvalue())
        await message.edit(result_text)
    except Exception as e:
        error_text = locale.get_text("eval", "error",
                             code=code, error_type=type(e).__name__, error_message=str(e))
        await message.edit(error_text)