from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class MusicPlayer:
    def __init__(self, playlist_with_durations, statusbar):
        self.playlist = playlist_with_durations
        self.statusbar = statusbar
        self.index = 0
        self.sound = None

    def next(self, dt=None):
        self.index += 1
        self.play_next()

    def play_next(self):
        if self.index >= len(self.playlist):
            self.index = 0

        song_name, duration, song = self.playlist[self.index]
        sound = SoundLoader.load(f"assets/audios/{song_name}.mp3")
        if sound:
            App.get_running_app().music_now = song
            Clock.schedule_once(
                lambda dt: self.statusbar.show_music(song),
                0
            )
            self.sound = sound
            self.sound.loop = False
            self.sound.play()
            Clock.schedule_once(self.next, duration)
        else:
            Clock.schedule_once(self.next, 0.5)
