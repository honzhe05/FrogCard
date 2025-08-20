from kivy.app import App
from kivy.clock import Clock

class PlayTimer:
    def __init__(self):
        self.app = App.get_running_app()
        self.seconds = 0
        self._event = None

    def set_time(self, h, m, s):
        self.seconds = h * 3600 + m * 60 + s
        self.resume()

    def _tick(self, dt):
        self.seconds += 1
        h, rem = divmod(self.seconds, 3600)
        m, s = divmod(rem, 60)
        self.app.h = h
        self.app.m = m
        self.app.s = s

    def get_time_str(self):
        return f"{self.app.h:02d}:{self.app.m:02d}:{self.app.s:02d}"

    def get_time_parts(self):
        return self.app.h, self.app.m, self.app.s

    def stop(self):
        if self._event:
            self._event.cancel()
            self._event = None

    def pause(self):
        self.stop()

    def resume(self):
        if not self._event:
            self._event = Clock.schedule_interval(self._tick, 1)