import random
import os
import math
from kivy.app import App
from kivy.uix.label import Label
from kivy.resources import resource_find
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window

class MovingFly(ButtonBehavior , Image):
    def __init__(self , money=None , **kwargs):
        super().__init__(**kwargs)
        self.money = money
        speed = random.uniform(2, 8)
        angle = random.uniform(0, 360)
        self.vx = speed * math.cos(math.radians(angle))
        self.vy = speed * math.sin(math.radians(angle))
        Clock.schedule_interval(self.move, 1/60)
        self.app = App.get_running_app()
        self._move_event = None
        
    def move(self , dt):
        if self.disabled:
            return
            
        self.x += self.vx 
        self.y += self.vy
        
        if self.x < 0 or self.x > Window.width - 100:
            self.vx *= -1
        if self.y < 200 or self.y > Window.height - 300:
            self.vy *= -1
    
    def on_release(self):
        try:
            if not self.disabled:
                self.app.mn += 5
    
                game_screen = self.app.root.get_screen('game')
                game_screen.money.text = str(self.app.mn)
                game_screen.money_hint("+5")
                self.app.root.get_screen('game').exp_bar.add_exp(18)
                game_screen.update_exp_level_label()
    
                self.source = resource_find('assets/Particle.png')
                fade_out = Animation(opacity=0, duration=0.5)
                fade_out.bind(on_complete=self.fade_complete)
                fade_out.start(self)
                self.disabled = True
                Clock.schedule_once(self.recover, 5)
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[MovingFly.on_release] {e}\n")

    def recover(self, dt):
        self.opacity = 1
        self.source = os.path.join('assets', 'Fly.png')
        self.disabled = False
        
        random_size = random.randint(140, 160)
        self.size = (random_size , random_size)
        self.pos = (
               random.randint(0 , Window.width - 100) ,
               random.randint(200 , Window.height - 300)
            )
            
    def fade_complete(self , animation , widget):
        widget.opacity = 0      
        
    def on_parent(self, widget, parent):
        if parent is None and self._move_event:
            Clock.unschedule(self._move_event)