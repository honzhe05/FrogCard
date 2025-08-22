# sound.py
from kivy.resources import resource_find
from kivy.core.audio import SoundLoader
from utils.error_handler import log_error
import threading


sound = None


def play_sound(name):
    global sound
    try:
        path = resource_find(f"assets/audios/{name}")
        if not path:
            return
        sound = SoundLoader.load(path)
        if sound:
            sound.play()
    except Exception as e:
        log_error("play_bgm", e)

def stop_bgm():
    global sound
    if sound and hasattr(sound, "stop"):
        sound.stop()

def play_sound_background(name):
    threading.Thread(target=play_sound, args=(name,), daemon=True).start()
    