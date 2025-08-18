from kivy.resources import resource_find
from kivy.core.audio import SoundLoader
import threading

def play_sound(name):
    sound = SoundLoader.load(resource_find('assets/' + name + '.wav'))
    if sound:
        print("Sound found at %s" % sound.source)
        print("Sound is %.3f seconds" % sound.length)
        sound.play()
        
def play_sound_background(name):
    threading.Thread(target=play_sound, args=(name,), daemon=True).start()