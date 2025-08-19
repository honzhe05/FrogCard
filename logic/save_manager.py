#save_manager.py
import json
import os
from kivy.app import App
from utils.error_handler import log_error

def get_save_path():
    try:
        base_path = App.get_running_app().user_data_dir
        return os.path.join(base_path, "savegame.json")
    except Exception as e:
        log_error("get_save_path", e)
        return "savegame.json" 

def ensure_data_dir():
    try:
        folder = os.path.dirname(get_save_path())
        os.makedirs(folder, exist_ok=True)
    except Exception as e:
        log_error("ensure_data_dir", e)

def save_game(money, diamond, xp, exp, level, quan, quan_level, quan_mn, xp_level, xp_mn, max_exp, buy_grass, buy_more_grass, buy_cloud, buy_tree, buy_apple, music, sound):
    game_data = {
        "money": money,
        "diamond": diamond,
        "xp": xp,
        "exp": exp,
        "level": level,
        "quan": quan,
        "quan_level": quan_level,
        "quan_mn": quan_mn,
        "xp_level": xp_level,
        "xp_mn": xp_mn,
        "max_exp": max_exp,
        "buy_grass": buy_grass,
        "buy_more_grass": buy_more_grass,
        "buy_cloud": buy_cloud,
        "buy_tree": buy_tree,
        "buy_apple": buy_apple,
        "music": music,
        "sound": sound
    }
    try:
        ensure_data_dir()
        with open(get_save_path(), "w", encoding="utf-8") as f:
            json.dump(game_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        log_error("save_game", e)

def load_game():
    default_data = {
        "money": 100,
        "diamond": 10,
        "xp": 2,
        "exp": 0,
        "level": 1,
        "quan": 5,
        "quan_level": 1,
        "quan_mn": 50,
        "xp_level": 1,
        "xp_mn": 100,
        "max_exp": 100,
        "buy_grass": True,
        "buy_more_grass": True,
        "buy_cloud": True,
        "buy_tree": True,
        "buy_apple": True,
        "music": 100,
        "sound": 100
    }
    try:
        path = get_save_path()
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, val in default_data.items():
                if key not in data:
                    data[key] = val
            return data
    except Exception as e:
        log_error("load_game", e)
    return default_data

def clear_save():
    try:
        path = get_save_path()
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        log_error("clear_save", e)