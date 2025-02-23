class SecurityError(Exception):
    pass

BLACKLIST = ["system(", "os.", "subprocess", "eval("]

def validate_code(code: str):
    for pattern in BLACKLIST:
        if pattern in code:
            raise SecurityError(f"Обнаружен запрещённый паттерн: {pattern}")
