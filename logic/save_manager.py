#save_manager.py
import json
import os
from utils.error_handler import log_error
from plyer import storagepath

try:
    bath_path = storagepath.get_documents_dir()
    SAVE_PATH = os.path.join(bath_path, "FrogCard", "data", "savegame.json")
except Exception as e:
    log_error("create_save_folder", e)

def ensure_data_dir():
    try:
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    except Exception as e:
        log_error("ensure_data_dir", e)

def save_game(money, diamond, exp, level, quan, quan_level, quan_mn, max_exp):
    game_data = {
        "money": money,
        "diamond": diamond,
        "exp": exp,
        "level": level,
        "quan": quan,
        "quan_level": quan_level,
        "quan_mn": quan_mn,
        "max_exp": max_exp
    }
    try:
        ensure_data_dir()
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(game_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        log_error("save_game", e)

def load_game():
    default_data = {
        "money": 100,
        "diamond": 10,
        "exp": 0,
        "level": 1,
        "quan": 5,
        "quan_level": 1,
        "quan_mn": 50,
        "max_exp": 100
    }
    if os.path.exists(SAVE_PATH) and os.path.getsize(SAVE_PATH) > 0:
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 確保必要欄位都有值
            for key, val in default_data.items():
                if key not in data:
                    data[key] = val
            return data
        except Exception as e:
            log_error("load_game", e)
    return default_data

def clear_save():
    try:
        if os.path.exists(SAVE_PATH):
            os.remove(SAVE_PATH)
    except Exception as e:
        log_error("clear_save", e)
