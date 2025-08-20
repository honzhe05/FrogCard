# bgm_player
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.index = 0
        self.sound = None
        self._checker = None

    def play_next(self, dt=0):
        if self.index >= len(self.playlist):
            self.index = 0

        song_name = self.playlist[self.index]
        sound = SoundLoader.load(f"assets/audios/{song_name}")
        if sound:
            self.sound = sound
            self.sound.loop = False
            self.sound.play()
            self.index += 1
            self._start_check()

    def _start_check(self):
        if self._checker:
            self._checker.cancel()
        self._checker = Clock.schedule_interval(self._check_finished, 0.5)

    def _check_finished(self, dt):
        if not self.sound or not self.sound.length:
            return
        if self.sound.get_pos() >= max(self.sound.length - 0.1, 0):
            self._checker.cancel()
            self.play_next()