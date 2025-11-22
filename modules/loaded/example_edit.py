# -*- coding: utf-8 -*-
import os
from pyrogram import Client
from command import Locale, fox_command, fox_sudo, who_message
filename = os.path.basename(__file__)
Module_Name = 'Example'


# If you need to install an external module via pip
# import the following line of code and install the library with the required parameter
#
# from requirements_installer import install_library
# install_library("requests -U") 
#
# ^^^ pip3 install requests -U
#
# =================================================
#
# from requirements_installer import install_library
# install_library("requests==2.32.3") 
#
# ^^^ pip3 install requests==2.32.3
#
# =================================================
#
# if you need to call any command after restarting
# with open("triggers/example_autostart", "w", encoding="utf-8") as f:
#        f.write("example_edit")
#        ^^^ enter the command that should be run after the userbot is restarted
#
# if you need write data config
# with open("userdata/example_config", "w", encoding="utf-8") as f:
#        f.write("example_data")
#        ^^^ enter the need data


en_strings = {
    'simple_text': '🦊 <b>This is a simple example module</b>',
    'text_with_var': '🎯 <b>Hello {name}! Module working.</b>'
}
ru_strings = {
    'simple_text': '🦊 <b>Это простой пример модуля</b>',
    'text_with_var': '🎯 <b>Привет {name}! Модуль работает.</b>'
}
ua_strings = {
    'simple_text': '🦊 <b>Це простий приклад модуля</b>',
    'text_with_var': '🎯 <b>Привіт {name}! Модуль працює.</b>'
}
locale = Locale(en=en_strings, ru=ru_strings, ua=ua_strings)


@Client.on_message(fox_command("example", Module_Name, filename) & fox_sudo())
async def example_simple(client, message):
    message = await who_message(client, message)
    text = locale.get_text("example", "simple_text")
    await message.edit(text)

@Client.on_message(fox_command("example_hello", Module_Name, filename, "[name]") & fox_sudo())
async def example_with_var(client, message):
    message = await who_message(client, message)
    args = message.text.split()
    name = args[1] if len(args) > 1 else "User"
    text = locale.get_text("example", "text_with_var", name=name)
    await message.edit(text)
