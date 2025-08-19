from kivy.resources import resource_find
from kivy.core.audio import SoundLoader
import threading
import time

def play_sound(name):
    try:
        path = resource_find(f"audios/{name}")
        if not path:
            print(f"❌ 找不到音效檔：{name}")
            return
        sound = SoundLoader.load(path)
        if sound:
            print(f"✅ 播放音效：{sound.source}（{sound.length:.3f} 秒）")
            sound.play()
            time.sleep(sound.length + 0.5)
    except Exception as e:
        print(f"❌ 播放失敗：{e}")

def play_sound_background(name):
    threading.Thread(target=play_sound, args=(name,), daemon=True).start()