import sys
import requests
import os
import json
from pprint import pprint
import re

from tools.security import SecurityError, validate_code
from tools.utils import get_cache_key, load_cache
from tools.config import API_URL, API_KEY, MODEL, CACHE_DIR, ASSEMBLER, LINKER

SYSTEM_PROMPT = """Ты конвертируешь код AILanguage в ассемблер для Windows x64. 
Требования:
1. Синтаксис NASM с директивой 'default rel'
2. Используй LEA для загрузки адресов
3. Стек: sub rsp,40 в начале, add rsp,40 перед ret
4. Все внешние функции объявлять как extern
5. Аргументы в RCX, RDX, R8, R9
6. Точно сохрани маркеры === ASM Code === и === End of ASM ===

Пример:
=== ASM Code ===
default rel
extern printf
...
lea rcx,[msg]
call printf
=== End of ASM ===
"""

def check_dependencies():
    # Проверка наличия NASM
    if os.system('nasm -v > nul 2>&1') != 0:
        raise Exception("NASM не установлен! Скачайте с https://nasm.us и добавьте в PATH")
    
    # Проверка наличия GCC
    if os.system('gcc --version > nul 2>&1') != 0:
        raise Exception("MinGW не установлен! Скачайте с https://winlibs.com и добавьте в PATH")

def sanitize_asm_code(code: str) -> str:
    """Исправление частых ошибок в ASM коде"""
    fixes = [
        (r'\bmov rcx,\[', 'lea rcx, ['),  # Замена MOV на LEA
        (r'^global start', 'global main'), # Исправление точки входа
        (r'sub rsp, 28h', 'sub rsp, 40'), # Правильное выравнивание
        (r'extern printf_', 'extern printf') # Исправление extern
    ]
    
    for pattern, replacement in fixes:
        code = re.sub(pattern, replacement, code, flags=re.M | re.I)
    
    if 'default rel' not in code:
        code = 'default rel\n' + code
    
    return code

def compile_ail(file_path, options):
    try:
        check_dependencies()  # Добавляем проверку зависимостей
        # Создаем директорию для кэша при запуске
        os.makedirs(CACHE_DIR, exist_ok=True)

        with open('docs/ail_reference_ru.ail', 'r', encoding='utf-8') as doc_file:
            docs = doc_file.read()
            
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        prompt = f"""
**Role**: Strict AILanguage Compiler
**Правила**:
1. Строго следуй документации:
{docs}

2. Для Windows:
   - Формат: PE64
   - Точка входа: main
   - Используй Windows API через kernel32.dll
   - Пример вызова: extern MessageBoxA

3. Общие требования:
   - Локальные метки для переходов
   - Оптимизация регистров
   - Комментарии для ключевых операций
   - Сохранение семантики исходного кода

**Пример вывода**:
=== ASM Code ===
section .data
    msg db 'Hello Windows!', 0
    fmt db '%s', 0

section .text
extern printf
extern ExitProcess

global main
main:
    push msg
    call printf
    add esp, 4
    xor eax, eax
    call ExitProcess
=== End of ASM ===

**Задача**:
Скомпилируй этот код AILanguage:
{code}
"""

        cache_key = get_cache_key(code)
        cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
        
        if cache_data := load_cache(cache_file):
            print(cache_data['output'])
            return

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "https://localhost",
            "X-Title": "AILanguage Compiler"
        }
        
        data = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        response = requests.post(API_URL, json=data, headers=headers, timeout=15)
        
        # Добавляем детальную проверку ответа
        if response.status_code != 200:
            error_msg = response.text
            if 'application/json' in response.headers.get('Content-Type', ''):
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', error_msg)
            raise ValueError(f"Ошибка API ({response.status_code}): {error_msg}")
            
        response_data = response.json()
        
        # Улучшенная проверка структуры ответа
        if not isinstance(response_data, dict) or 'choices' not in response_data:
            raise ValueError(
                f"Некорректный формат ответа API. Получено: {response.text[:200]}"
            )
            
        if len(response_data['choices']) == 0:
            raise ValueError("Пустой ответ от ИИ-модели")
            
        result = response_data['choices'][0]['message']['content']
        
        # Извлекаем только ASM код между маркерами
        asm_start = result.find('=== ASM Code ===')
        asm_end = result.find('=== End of ASM ===')
        
        if asm_start == -1 or asm_end == -1:
            raise Exception("ИИ не сгенерировал корректный ASM код")
            
        clean_output = result[asm_start+len('=== ASM Code ==='):asm_end].strip()
        clean_output = sanitize_asm_code(clean_output)  # Добавляем санитайзинг
        
        # Удаляем комментарии ИИ
        clean_output = '\n'.join([line for line in clean_output.split('\n') 
                                if not line.strip().startswith(';') 
                                and not line.strip().startswith('#')])

        if options.get('output'):
            with open(options['output'], 'w', encoding='utf-8') as f:
                f.write(clean_output)
            print(f"Скомпилировано в {options['output']}")
        else:
            print(clean_output)
        
        # Сохраняем в кэш
        with open(cache_file, 'w') as f:
            json.dump({'output': clean_output}, f)

        # После получения ASM кода
        output_dir = os.path.dirname(options['output']) if options.get('output') else os.path.dirname(file_path)
        base_name = os.path.basename(options['output'] if options.get('output') else file_path)
        base_name = os.path.splitext(base_name)[0]

        # Исправление: Создаем выходную директорию если не существует
        os.makedirs(output_dir, exist_ok=True)

        asm_file = os.path.join(output_dir, f"{base_name}.asm")
        obj_file = os.path.join(output_dir, f"{base_name}.o")
        exe_file = os.path.join(output_dir, base_name)

        # Записываем ASM
        with open(asm_file, 'w', encoding='utf-8') as f:
            f.write(clean_output)
            print(f"ASM код сохранён в {asm_file}")  # Логирование

        # Для Windows x64
        if os.name == 'nt':
            obj_file = os.path.join(output_dir, f"{base_name}.obj")
            exe_file += ".exe"
            
            # Команда ассемблирования
            assemble_cmd = f'nasm -f win64 "{asm_file}" -o "{obj_file}"'
            
            # Команда линковки с явным указанием точки входа
            link_cmd = f'gcc -m64 -o "{exe_file}" "{obj_file}" -Wl,-subsystem,console -lkernel32 -lmsvcrt'
            
            print(f"Ассемблируем: {asm_file} -> {obj_file}")
            if os.system(assemble_cmd) != 0:
                raise Exception("Ошибка NASM! Проверьте:\n1. Установлен NASM 2.14+\n2. Команда: " + assemble_cmd)
            
            print(f"Линкуем: {obj_file} -> {exe_file}")
            if os.system(link_cmd) != 0:
                raise Exception("Ошибка GCC! Проверьте:\n1. MinGW x64 установлен\n2. Команда: " + link_cmd)
        else:
            # Существующий Linux код
            os.system(f'nasm -f elf64 {asm_file}')
            os.system(f'ld -m elf_x86_64 -s -o {exe_file} {obj_file}')
        
        print(f"Создан исполняемый файл: {exe_file}")

    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {str(e)}")
        print(f"Сырой ответ: {response.text[:500]}")
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка: {str(e)}")
    except KeyError as e:
        print(f"Ошибка формата ответа: отсутствует ключ {str(e)}")
    except Exception as e:
        print(f"\nОшибка выполнения: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python compiler.py <file.ail>")
        sys.exit(1)

    options = {
        'output': None,
        'execute': True
    }
    
    for i, arg in enumerate(sys.argv[1:-1]):
        if arg in ['-o', '--output']:
            options['output'] = sys.argv[i+2]
        elif arg == '--no-execute':
            options['execute'] = False

    file_path = sys.argv[-1]
    compile_ail(file_path, options)
