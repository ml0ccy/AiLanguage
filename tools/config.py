import os

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "API_KEY_FROM_OPENROUTER.AI"
# Важно выбирать качественную модель
# От этого зависит качество .asm кода и понимание .ail
MODEL = "google/gemini-2.0-pro-exp-02-05:free"
CACHE_DIR = ".ail_cache"
LINKER = "gcc" if os.name == 'nt' else "ld"
ASSEMBLER = "nasm -f win64"
DOCS_PATH = "docs/ail_reference_ru.ail"
SUFFIX = ".exe"
