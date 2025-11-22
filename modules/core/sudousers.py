# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

from pyrogram import Client, filters

from command import Locale, fox_command, who_message, my_prefix
from modules.core.restarter import restart

SUDO_USERS_FILE = Path("userdata/sudo_users.json")

en_strings = {
    "usage": """<emoji id='5283051451889756068'>🦊</emoji> <b>Usage:</b>
<code>{prefix}sudo add @username</code>
<code>{prefix}sudo del @username</code>
<code>{prefix}sudo list</code>""",
    "list_title": "<emoji id='5283051451889756068'>🦊</emoji> <b>Sudo users:</b>\n<blockquote expandable>{users_list}</blockquote>",
    "no_users": "No sudo users",
    "specify_user": "<emoji id='5210952531676504517'>❌</emoji> <b>Please specify a user!</b>",
    "user_not_found": "<emoji id='5210952531676504517'>❌</emoji> <b>User not found!</b>",
    "already_in_list": "<emoji id='5210952531676504517'>❌</emoji> <b>User <code>{user}</code> is already in the list!</b>",
    "added": "<emoji id='5237699328843200968'>✅</emoji>  <b>User <code>{user}</code> added to sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Rebooting...",
    "removed": "<emoji id='5237699328843200968'>✅</emoji>  <b>User <code>{user}</code> removed from sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Rebooting...",
    "not_found": "<emoji id='5210952531676504517'>❌</emoji> <b>User <code>{user}</code> not found in the list!</b>",
    "unknown_action": "<emoji id='5210952531676504517'>❌</emoji> <b>Unknown action! Use add/del/list</b>"
}
ru_strings = {
    "usage": """<emoji id='5283051451889756068'>🦊</emoji> <b>Использование:</b>
<code>{prefix}sudo add @username</code>
<code>{prefix}sudo del @username</code>
<code>{prefix}sudo list</code>""",
    "list_title": "<emoji id='5283051451889756068'>🦊</emoji> <b>Sudo пользователи:</b>\n<blockquote expandable>{users_list}</blockquote>",
    "no_users": "Нет sudo пользователей",
    "specify_user": "<emoji id='5210952531676504517'>❌</emoji> <b>Укажите пользователя!</b>",
    "user_not_found": "<emoji id='5210952531676504517'>❌</emoji> <b>Пользователь не найден!</b>",
    "already_in_list": "<emoji id='5210952531676504517'>❌</emoji> <b>Пользователь <code>{user}</code> уже в списке!</b>",
    "added": "<emoji id='5237699328843200968'>✅</emoji>  <b>Пользователь <code>{user}</code> добавлен в sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Перезагружаю...",
    "removed": "<emoji id='5237699328843200968'>✅</emoji>  <b>Пользователь <code>{user}</code> удален из sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Перезагружаю...",
    "not_found": "<emoji id='5210952531676504517'>❌</emoji> <b>Пользователь <code>{user}</code> не найден в списке!</b>",
    "unknown_action": "<emoji id='5210952531676504517'>❌</emoji> <b>Неизвестное действие! Используйте add/del/list</b>"
}
ua_strings = {
    "usage": """<emoji id='5283051451889756068'>🦊</emoji> <b>Використання:</b>
<code>{prefix}sudo add @username</code>
<code>{prefix}sudo del @username</code>
<code>{prefix}sudo list</code>""",
    "list_title": "<emoji id='5283051451889756068'>🦊</emoji> <b>Sudo користувачі:</b>\n<blockquote expandable>{users_list}</blockquote>",
    "no_users": "Немає sudo користувачів",
    "specify_user": "<emoji id='5210952531676504517'>❌</emoji> <b>Вкажіть користувача!</b>",
    "user_not_found": "<emoji id='5210952531676504517'>❌</emoji> <b>Користувача не знайдено!</b>",
    "already_in_list": "<emoji id='5210952531676504517'>❌</emoji> <b>Користувач <code>{user}</code> вже у списку!</b>",
    "added": "<emoji id='5237699328843200968'>✅</emoji>  <b>Користувача <code>{user}</code> додано до sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Перезавантажую...",
    "removed": "<emoji id='5237699328843200968'>✅</emoji>  <b>Користувача <code>{user}</code> видалено з sudo!</b>\n<emoji id='5264727218734524899'>🔄</emoji> Перезавантажую...",
    "not_found": "<emoji id='5210952531676504517'>❌</emoji> <b>Користувача <code>{user}</code> не знайдено у списку!</b>",
    "unknown_action": "<emoji id='5210952531676504517'>❌</emoji> <b>Невідома дія! Використовуйте add/del/list</b>"
}

locale = Locale(en=en_strings, ru=ru_strings, ua=ua_strings)

def load_sudo_users():
    with open(SUDO_USERS_FILE, "r") as f:
        return json.load(f)

def save_sudo_users(users):
    with open(SUDO_USERS_FILE, "w") as f:
        json.dump(users, f)

@Client.on_message(fox_command("sudo", "SudoManager", os.path.basename(__file__), "[add/del/list] [@username/id]") & filters.me)
async def sudo_manager(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=2)
    
    if len(args) < 2:
        usage_text = locale.get_text("sudo", "usage", prefix=my_prefix())
        return await message.edit(usage_text)

    action = args[1].lower()
    sudo_users = load_sudo_users()

    if action == "list":
        users_list = "\n".join([f"• <code>{user}</code>" for user in sudo_users]) or locale.get_text("sudo", "no_users")
        list_text = locale.get_text("sudo", "list_title", users_list=users_list)
        return await message.edit(list_text)

    if len(args) < 3:
        specify_text = locale.get_text("sudo", "specify_user")
        return await message.edit(specify_text)

    user_input = args[2].strip()
    user_id = None

    if user_input.startswith("@"):
        try:
            user = await client.get_users(user_input)
            user_id = int(user.id)
        except Exception:
            not_found_text = locale.get_text("sudo", "user_not_found")
            return await message.edit(not_found_text)
    else:
        user_id = user_input  

    if action == "add":
        if int(user_id) in sudo_users:
            already_text = locale.get_text("sudo", "already_in_list", user=user_input)
            await message.edit(already_text)
        else:
            sudo_users.append(int(user_id))
            save_sudo_users(sudo_users)
            added_text = locale.get_text("sudo", "added", user=user_input)
            await message.edit(added_text)
            await restart(message, restart_type="restart")

    elif action == "del":
        if int(user_id) in sudo_users:
            sudo_users.remove(int(user_id))
            save_sudo_users(sudo_users)
            removed_text = locale.get_text("sudo", "removed", user=user_input)
            await message.edit(removed_text)
            await restart(message, restart_type="restart")
        else:
            not_found_text = locale.get_text("sudo", "not_found", user=user_input)
            await message.edit(not_found_text)

    else:
        unknown_text = locale.get_text("sudo", "unknown_action")
        await message.edit(unknown_text)