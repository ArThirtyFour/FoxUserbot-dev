import configparser
import json
import os
from pathlib import Path
from typing import List, Union
from pyrogram import filters
from pyrogram.types import ReplyParameters
from modules.core.settings.main_settings import add_command_help, file_list


_PREFIX = None
_GLOBAL_LANG = None


def my_prefix():
    global _PREFIX
    if _PREFIX is not None:
        return _PREFIX
        
    PATH_FILE = "userdata/config.ini"
    Path("userdata").mkdir(exist_ok=True)

    config = configparser.ConfigParser()
    if os.path.exists(PATH_FILE):
        config.read(PATH_FILE)
    else:
        config.add_section("prefix")
        config.set("prefix", "prefix", "!")
        with open(PATH_FILE, "w") as config_file:
            config.write(config_file)
    
    try:
        _PREFIX = config.get("prefix", "prefix")
    except:
        _PREFIX = "!"
    
    return _PREFIX


# alias
def load_aliases() -> dict:
    try:
        if os.path.exists("userdata/command_aliases.json"):
            with open("userdata/command_aliases.json", 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

# sudo check
async def who_message(client, message):
    me = await client.get_me()
    if message.from_user.id == me.id:
        return message
    else:
        try:
            reply_id = message.reply_to_message.id
        except:
            reply_id = message.id
        return await client.send_message(
            message.chat.id, 
            message.text, 
            message_thread_id=message.message_thread_id,
            reply_parameters=ReplyParameters(message_id=reply_id)
        )

# sudo trigger
def fox_sudo():
    sudo_file = Path("userdata/sudo_users.json")
    sudo_users_list = []
    try:
        with open(sudo_file, 'r', encoding='utf-8') as f:
            sudo_users_list = json.load(f)
            i = (filters.user(sudo_users_list) or filters.chat(sudo_users_list))
            return i
    except:
        return filters.me

def fox_command(
    command: Union[str, List[str]], 
    module_name: str, 
    filename: str, 
    arguments: str = ""
) -> filters.Filter:
    module_name = module_name.replace(" ", "_")
    commands = [command] if isinstance(command, str) else command.copy()
    aliases = load_aliases()

    alias_list = []
    for cmd in commands:
        for alias, target_cmd in aliases.items():
            if target_cmd.startswith(f"{my_prefix()}{cmd}") or target_cmd == cmd:
                alias_list.append(alias)
    
    all_commands = commands + alias_list
    
    help_text = " | ".join(f"{my_prefix()}{cmd} {arguments}".strip() for cmd in commands)
    if alias_list:
        help_text += f" (Aliases: {my_prefix()}{f', {my_prefix()}'.join(alias_list)})"
    
    add_command_help(module_name, help_text)
    file_list[module_name] = filename
    
    return filters.command(all_commands, prefixes=my_prefix())


class Locale():

    all_lang = ["en", "ru", "ua"]
    default_lang = "en"
    _GLOBAL_LANG = None
    _instance = None

    def __init__(self, **languages):

        self.languages = {}
        for code, bundle in (languages or {}).items():
            if isinstance(bundle, dict):
                self.languages[code.lower()] = bundle
    def set_global_lang(self, lang: str) -> bool:
        if lang not in self.all_lang:
            return False

        self._GLOBAL_LANG = lang
        lang_config_path = Path("userdata/language.ini")
        lang_config_path.parent.mkdir(exist_ok=True)

        config = configparser.ConfigParser()
        if lang_config_path.exists():
            config.read(lang_config_path)

        if not config.has_section("language"):
            config.add_section("language")
        config.set("language", "lang", lang)

        with open(lang_config_path, "w") as f:
            config.write(f)

        return True
    
    def get_available_langs(self) -> list:
        return self.all_lang
    
    def get_text(self, module: str, key: str, LANGUAGES: dict = None, **kwargs) -> str:
        bundles = LANGUAGES if LANGUAGES is not None else getattr(self, "languages", {})
        if bundles:
            return self.get_module_text(key, bundles, **kwargs)
        return key
    
    def get_module_text(self, key: str, LANGUAGES: dict, **kwargs) -> str:
        lang = self.get_global_lang()
        bundle = LANGUAGES.get(lang) or LANGUAGES.get("en", {})
        text = bundle.get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text

    def get_global_lang(self) -> str:
        if self._GLOBAL_LANG is not None:
            return self._GLOBAL_LANG

        lang_config_path = Path("userdata/language.ini")
        Path("userdata").mkdir(exist_ok=True)

        if lang_config_path.exists():
            config = configparser.ConfigParser()
            config.read(lang_config_path)
            try:
                lang = config.get("language", "lang", fallback=self.default_lang)
                lang = lang.lower()
                if lang in self.all_lang:
                    self._GLOBAL_LANG = lang
                    return self._GLOBAL_LANG
            except Exception:
                pass

        self._GLOBAL_LANG = self.default_lang
        return self._GLOBAL_LANG


temp_locale = Locale()
all_lang = Locale.all_lang

def get_global_lang() -> str:
    return temp_locale.get_global_lang()

def set_global_lang(lang: str) -> bool:
    return temp_locale.set_global_lang(lang)

def get_text(module: str, key: str, LANGUAGES: dict = None, **kwargs) -> str:
    return temp_locale.get_text(module, key, LANGUAGES, **kwargs)

def get_available_langs() -> list:
    return temp_locale.get_available_langs()

def configure_locale(**languages):
    temp_locale.configure(**languages)

