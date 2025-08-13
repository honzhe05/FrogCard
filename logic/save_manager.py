import json
import os
import traceback
from kivy.app import App

SAVE_PATH = "data/savegame.json"
ERROR_LOG = "error.log"

def log_error(prefix, e):
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{prefix}] {str(e)}\n")
        f.write(traceback.format_exc() + "\n")

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
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(game_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        log_error("save_game", e)

def load_game():
    if os.path.exists(SAVE_PATH) and os.path.getsize(SAVE_PATH) > 0:
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                "money": data.get("money", 100),
                "diamond": data.get("diamond", 10),
                "exp": data.get("exp", 0),
                "level": data.get("level", 1),
                "quan": data.get("quan", 5),
                "quan_level": data.get("quan_level", 1),
                "quan_mn": data.get("quan_mn", 50),
                "max_exp": data.get("max_exp", 100)
            }
        except Exception as e:
            log_error("load_game", e)
    return {
        "money": 100,
        "diamond": 10,
        "exp": 0,
        "level": 1,
        "quan": 5,
        "quan_level": 1,
        "quan_mn": 50,
        "max_exp": 100
    }

def clear_save():
    try:
        if os.path.exists(SAVE_PATH):
            os.remove(SAVE_PATH)
    except Exception as e:
        log_error("clear_save", e)