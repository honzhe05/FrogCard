#fly.py
import random
import math
import logic.sound
from kivy.app import App
from kivy.resources import resource_find
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from utils.error_handler import log_error

class MovingFly(ButtonBehavior, Image):
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
                self.xp = int(self.app.xp)
                if self.size[0] < 91 and self.size[0] > 60:
                    self.app.mn += self.xp * 2
                    self.size_mn = self.xp * 2
                elif self.size[0] < 61:
                    self.app.mn += self.xp * 5
                    self.size_mn = self.xp * 5
                else:
                    self.app.mn += self.xp
                    self.size_mn = self.xp
        
                game_screen = self.app.root.get_screen('game')
                shop_panel = self.app.root.get_screen('shop')
                decorate_screen = self.app.root.get_screen('decorate')
                game_screen.status_bar.money.text = str(self.app.mn)
                shop_panel.status_bar.money.text = str(self.app.mn)
                decorate_screen.status_bar.money.text = str(self.app.mn)
                game_screen.status_bar.money_hint("+" + str(self.size_mn))
                self.app.root.get_screen('game').status_bar.exp_bar.add_exp(18)
                game_screen.status_bar.update_exp_level_label()
                shop_panel.status_bar.update_exp_level_label()
                decorate_screen.status_bar.update_exp_level_label()
    
                self.source = resource_find('assets/Particle.png')
                fade_out = Animation(opacity=0, duration=0.5)
                fade_out.bind(on_complete=self.fade_complete)
                fade_out.start(self)
                self.disabled = True
                logic.sound.play_sound_background("GotFly")
                Clock.schedule_once(self.recover, 5)
        except Exception as e:
            log_error("MovingFly.on_release", e)

    def recover(self, dt):
        self.opacity = 1
        self.source = resource_find('assets/Fly.png')
        self.disabled = False
        
        random_size = random.randint(50, 250)
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