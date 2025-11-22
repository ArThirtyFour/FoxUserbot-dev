# ТУТ VERY BIG VIBECODE МНЕ ПОХУЙ ДРОЧИ МАНГО НОГАМИ Я ВЫГЛЯЖУ КАК ТЕТО ТРАХЕР

import os
import re
import ast
import pprint

def convert_module_new_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    module_name_match = re.search(r"module_list\['([^']+)'\]", content)
    if not module_name_match:
        return
    
    module_name = module_name_match.group(1)
    
    content = re.sub(r"module_list\['[^']+'\].*?\n", "", content)
    content = re.sub(r"file_list\['[^']+'\].*?\n", "", content)
    
    content = re.sub(r"^from command import fox_command\s*\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^import os\s*\n?", "", content, flags=re.MULTILINE)
    
    new_imports = "from command import fox_command\nimport os\n\n"
    content = new_imports + content.lstrip()
    
    if "filename = os.path.basename(__file__)" not in content:
        insert_pos = 0
        lines = content.splitlines(keepends=True)
        
        for i, line in enumerate(lines):
            if not line.strip() or line.startswith(("from ", "import ")):
                continue
            insert_pos = i
            break
        
        new_code = "filename = os.path.basename(__file__)\nModule_Name = '{}'\n\n".format(module_name)
        content = "".join(lines[:insert_pos] + [new_code] + lines[insert_pos:])
    
    content = re.sub(
        r'filters\.command\(([\'"\[\]])([^\)]+)\1\s*,\s*prefixes\s*=\s*my_prefix\(\)\)',
        lambda m: f'fox_command({m.group(1)}{m.group(2)}{m.group(1)}, Module_Name, filename)',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"File {file_path} converted!")


def convert_module_filters_me(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Проверяем наличие необходимых импортов
    has_fox_sudo = "fox_sudo" in content
    has_who_message = "who_message" in content
    has_fox_command = "fox_command" in content

    content = content.replace("message = await who_message(client, message, message.reply_to_message)", "message = await who_message(client, message)")
    content = content.replace("from prefix import my_prefix", "from command import my_prefix")
    content = content.replace("from modules.plugins_1system", "from modules.core")
    

    # Умное добавление импортов
    if "from command import" in content and not (has_fox_sudo and has_who_message):
        content = re.sub(
            r'(from command import)([^\n]*)',
            lambda m: m.group(0) + 
                     ('' if has_fox_sudo else ', fox_sudo') + 
                     ('' if has_who_message else ', who_message'),
            content,
            count=1
        )
        # Обновляем флаги после добавления импортов
        has_fox_sudo = has_fox_sudo or "fox_sudo" in content
        has_who_message = has_who_message or "who_message" in content
    
    # Заменяем только filters.me без ~ перед ним
    if has_fox_sudo:
        def safe_replace(match):
            before = match.group(1)
            after = match.group(2)
            if not before.rstrip().endswith('~'):
                if after and after[0] in (' ', '&', '|', ')', '\n'):
                    return f'@Client.on_message({before}fox_sudo(){after}'
            return match.group(0)
        
        content = re.sub(
            r'@Client\.on_message\((.*?)filters\.me([^a-zA-Z0-9_]*)',
            safe_replace,
            content
        )
    
    # Умное добавление who_message в функции
    if has_who_message:
        def add_who_message(match):
            decorator = match.group(1)
            func_block = match.group(2)
            
            # Проверяем, есть ли fox_command в декораторе
            needs_who_message = "fox_command" in decorator
            
            if needs_who_message and 'message = await who_message(client, message)' not in func_block:
                func_block = re.sub(
                    r'(async def \w+\(client, message\):\n)',
                    r'\1    message = await who_message(client, message)\n',
                    func_block,
                    count=1
                )
            return decorator + func_block
        
        content = re.sub(
            r'(@Client\.on_message\(.*?\)\n)(async def \w+\(client, message\):[\s\S]*?(?=\n\n|\Z))',
            add_who_message,
            content
        )
    
    content = content.replace("message.command[", "message.text.split()[")
                
    content = re.sub(
        r'async def (\w+)\(client: Client, message: Message\)',
        r'async def \1(client, message)',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def convert_locales(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'LANGUAGES' not in content:
            new_content = _rewrite_get_text_calls(content)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            return

        tree = ast.parse(content)
        lang_assign = None
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id == 'LANGUAGES':
                        if isinstance(node.value, ast.Dict):
                            lang_assign = node
                            break
            if lang_assign:
                break

        if not lang_assign:
            new_content = _rewrite_get_text_calls(content)
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            return

        start_line = lang_assign.lineno - 1
        start_col = lang_assign.col_offset
        end_line = getattr(lang_assign, 'end_lineno', None)
        end_col = getattr(lang_assign, 'end_col_offset', None)
        lines = content.splitlines(True)
        if end_line is None or end_col is None:
            start_idx = sum(len(l) for l in lines[:start_line]) + start_col
            snippet = content[start_idx:]
            brace = 0
            end_idx = None
            for i, ch in enumerate(snippet):
                if ch == '{':
                    brace += 1
                elif ch == '}':
                    brace -= 1
                    if brace == 0:
                        end_idx = i + 1
                        break
            if end_idx is None:
                return
            assign_text = content[start_idx:start_idx + end_idx]
            assign_start = start_idx
            assign_end = start_idx + end_idx
        else:
            assign_start = sum(len(l) for l in lines[:start_line]) + start_col
            assign_end = sum(len(l) for l in lines[:end_line - 1]) + end_col
            assign_text = content[assign_start:assign_end]

        try:
            eq_pos = assign_text.find('=')
            rhs = assign_text[eq_pos + 1:].strip()
            lang_dict = ast.literal_eval(rhs)
            if not isinstance(lang_dict, dict):
                return
        except Exception:
            return

        ordered_codes = [code for code in ['en', 'ru', 'ua'] if code in lang_dict] + [code for code in lang_dict.keys() if code not in ('en', 'ru', 'ua')]
        lang_blocks = []
        for code in ordered_codes:
            block = f"{code}_strings = {pprint.pformat(lang_dict[code], width=120, compact=False)}\n"
            lang_blocks.append(block)
        lang_code = ''.join(lang_blocks) + f"locale = Locale({', '.join([f'{code}={code}_strings' for code in ordered_codes])})\n"

        content2 = content[:assign_start] + lang_code + content[assign_end:]

        if 'from command import Locale' not in content2:
            if re.search(r'^from\s+command\s+import\s+.*$', content2, flags=re.MULTILINE):
                content2 = re.sub(
                    r'^(from\s+command\s+import\s+)(.*)$',
                    lambda m: m.group(1) + (m.group(2) + ', Locale' if 'Locale' not in m.group(2) else m.group(2)),
                    content2,
                    count=1,
                    flags=re.MULTILINE,
                )
            else:
                lines2 = content2.splitlines(True)
                insert_pos = 0
                for i, line in enumerate(lines2):
                    if line.startswith(('from ', 'import ')) or not line.strip():
                        insert_pos = i + 1
                    else:
                        break
                lines2.insert(insert_pos, 'from command import Locale\n')
                content2 = ''.join(lines2)

        content3 = _rewrite_get_text_calls(content2)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content3)
        print(f"Locales converted in {file_path}")
    except Exception as e:
        print(f"Locales conversion failed for {file_path}: {e}")


def _rewrite_get_text_calls(content: str) -> str:
    s = content
    s = re.sub(r'\bLocale\.get_text\s*\(', 'locale.get_text(', s)
    s = re.sub(r'(?<!\.)\bget_text\s*\(', 'locale.get_text(', s)
    s = re.sub(r',\s*LANGUAGES\s*=\s*LANGUAGES', '', s)
    s = re.sub(r'\(\s*LANGUAGES\s*=\s*LANGUAGES\s*,\s*', '(', s)
    s = re.sub(r'\(\s*LANGUAGES\s*=\s*LANGUAGES\s*\)', '()', s)
    return s

def check_duplicate(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        

        if not os.path.isfile(file_path) or not filename.endswith('.py'):
            continue

        new_name = re.sub(r'[()]', '', filename.replace(' ', '_'))

        if new_name != filename:
            new_path = os.path.join(folder_path, new_name)
            try:
                os.rename(file_path, new_path)
                print(f'Renamed: {filename} -> {new_name}')
            except Exception as f:
                print(f)


def process_modules_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                convert_module_new_format(file_path)
                convert_module_filters_me(file_path)
                convert_locales(file_path)
    check_duplicate(directory)

def convert_modules():
    process_modules_directory("modules/loaded")

convert_modules()


