import os
import json

COOKIE_FILE = os.path.join(os.path.dirname(__file__), '../data/cookie.json')

def get_cookie():
    """获取存储的cookie"""
    try:
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cookie', '')
    except Exception:
        return ''

def save_cookie(cookie):
    """保存cookie"""
    try:
        # 确保data目录存在
        os.makedirs(os.path.dirname(COOKIE_FILE), exist_ok=True)
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'cookie': cookie}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
