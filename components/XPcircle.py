from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse , Line
from kivy.app import App

class ExpArc(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.current_exp = 0

        self.bind(pos=self.update_arc, size=self.update_arc)

    def get_angle(self):
         return 90 + 90 * (self.current_exp / self.app.max_exp)

    def update_arc(self, *args):
        self.canvas.clear()
        size = min(self.width, self.height)
    
        with self.canvas:
            Color(0.2, 0.8, 0.2, 1)
            Line(
                circle=(self.center_x, self.center_y, size / 2, 90, self.get_angle()),
                width=10
            )
            
    def add_exp(self, amount):
        try:
            self.current_exp += amount
            while self.current_exp >= self.app.max_exp:
                self.current_exp -= self.app.max_exp
                self.app.level += 1
                self.app.max_exp = int(self.app.max_exp * 1.1)
            self.update_arc()
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[ExpArc.add_exp] {e}\n")