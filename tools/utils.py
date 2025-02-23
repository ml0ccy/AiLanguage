import hashlib
import os
import json

def get_cache_key(code: str) -> str:
    return hashlib.md5(code.encode()).hexdigest()

def save_cache(cache_key: str, data: dict):
    os.makedirs(os.path.dirname(cache_key), exist_ok=True)
    with open(cache_key, 'w') as f:
        json.dump(data, f)

def load_cache(cache_key: str) -> dict:
    if os.path.exists(cache_key):
        with open(cache_key, 'r') as f:
            return json.load(f)
    return None
