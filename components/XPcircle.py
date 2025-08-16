#XPcircle.py
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse , Line
from kivy.app import App
from utils.error_handler import log_error
from kivy.clock import Clock

class ExpArc(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
        self.bind(pos=self.update_arc, size=self.update_arc)

    def get_angle(self):
         return 90 + 90 * (self.app.exp / self.app.max_exp)

    def update_arc(self, *args):
        size = min(self.width, self.height)
        
        self.canvas.clear()
        with self.canvas:
            Color(0.2, 0.8, 0.2, 1)
            Line(
                circle=(self.center_x, self.center_y, size / 2, 90, self.get_angle()),
                width=10
            )
            
    def add_exp(self, amount):
        try:
            self.app.exp += amount
            while self.app.exp >= self.app.max_exp:
                self.app.exp -= self.app.max_exp
                self.app.level += 1
                self.app.max_exp = 100 * (1.12 ** int(self.app.level))
            Clock.schedule_once(lambda dt: self.update_arc(), 0)
        except Exception as e:
            log_error("ExpArc.add_exp", e)