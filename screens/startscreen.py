import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from components.imagebutton import ImageButton

class StartScreen(Screen):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.app = App.get_running_app()
        
        #background
        background = Image(
            source = os.path.join('assets' , 'Background.jpg') ,
            size_hint = (1 , 1) ,
            pos = (0 , 0) ,
            allow_stretch = True ,
            keep_ratio = False
        )
        layout.add_widget(background)
        
        #title
        img_width = Window.width * 0.85
        center_x = (Window.width - img_width) / 2
        center_y = Window.height * 0.22
      
        self.title = ImageButton(
            source = os.path.join('assets' ,  'Title.png') ,
            size_hint = (0.85, 0.85),
            pos = (center_x, center_y),
            allow_stretch = True ,
            keep_ratio = True
        )
        
        layout.add_widget(self.title)
        self.title.bind(on_release = self.title_change_image)
        
        #title frog
        self.titlefrog = Image(
            source = os.path.join('assets' , 'titlefrog.png') ,
            size_hint= (0.15, 0.15),
            pos = (Window.width, -50) ,
            allow_stretch = True ,
            keep_ratio = True
        )
        layout.add_widget(self.titlefrog)
        
        #start button
        img_width = Window.width * 0.3
        center_x = (Window.width - img_width) / 2
        center_y = Window.height * 0.05
        
        self.startbtn = ImageButton(
            source = os.path.join('assets' , 'StartButton.png') ,
            size_hint = (0.4, 0.4) ,
            pos = (img_width, center_y),
            allow_stretch = True ,
            keep_ratio = True
        )
        layout.add_widget(self.startbtn)
        self.startbtn.bind(on_release = self.go_to_game)
    
        self.add_widget (layout)
        
        self.start_jump_animation()
        
    def title_anim(self):
            base_y = Window.height * 0.03
            offset = self.title.y
            self.anim_up = Animation(y = offset + base_y , duration = 0.5)
            self.anim_down = Animation(y = offset , duration = 0.8)
            self.anim = self.anim_up + self.anim_down
            self.anim.repeat = True
            self.anim.start(self.title)
        
    def title_change_image(self, *args):
        try:
            self.anim.stop(self.title)
            self.title.source = os.path.join('assets', 'Titleb.png')
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[title_change_image] {e}\n")

    def start_jump_animation(self):
        try:
            anim = Animation(x=self.titlefrog.x - Window.width - 200, duration=4.5)
            anim.bind(on_complete=self.reset_position)
            anim.start(self.titlefrog)
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[start_jump_animation] {e}\n")

    def reset_position(self, *args):
        self.titlefrog.x = Window.width
        self.start_jump_animation()
        
    def go_to_game(self, *args):
        self.anim_btn = Animation(opacity = 0, duration = 0.2)
        self.anim_btn.bind(on_complete = lambda *_: self.contin())
        self.anim_btn.start(self.startbtn)
        
    def contin(self):
       self.manager.current = 'game'
       
    def on_enter(self):
        self.title_anim()

    def on_leave(self, *args):
        self.anim.stop(self.title)