import re

def validate_asm_syntax(code: str):
    """Проверка ключевых требований к ASM коду"""
    checks = [
        ('default rel', 'Отсутствует default rel'),
        ('sub rsp,40', 'Неправильное выравнивание стека'),
        ('lea rcx', 'Используй LEA вместо MOV для адресов'),
        ('global main', 'Неверная точка входа'),
        ('extern ', 'Отсутствуют extern объявления')
    ]
    
    for pattern, error_msg in checks:
        if not re.search(pattern, code, re.IGNORECASE):
            raise AssertionError(f"Ошибка: {error_msg}") 