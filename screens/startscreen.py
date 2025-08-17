#statrscreen.py
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_find
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from components.imagebutton import ImageButton
from utils.error_handler import log_error
from config import FULL_VERSION

class StartScreen(Screen):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.app = App.get_running_app()
        
        #background
        background = Image(
            source = resource_find('assets/Background.jpg') ,
            size_hint = (1, 1) ,
            pos = (0 , 0),
            allow_stretch = True,
            keep_ratio = False
        )
        layout.add_widget(background)
        
        #version
        version_text = Label(
            text=(f"[size=30]Game Version: {FULL_VERSION}\n"
                  "[size=28]Did you know? I created two new bugs while trying to fix one.\n"
                  "[size=28]Spent over two hours tweaking and debugging... still couldn't fix it.\n"
                  "[size=28]Game Developer: Honzhe, AvianJay and copilot. wait nooo\n"),
            markup = True,
            font_name='NotoSans-Light',
            size_hint=(None, None),
            size=(Window.width * 0.8, Window.height * 0.01),
            font_size=30,
            pos_hint={'x': 0, 'y': 0.94},
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        version_text.bind(size=version_text.setter('text_size'))
        layout.add_widget(version_text)
        
        #title
        img_width = Window.width * 0.85
        center_x = (Window.width - img_width) / 2
        center_y = Window.height * 0.22
      
        self.title = ImageButton(
            source = resource_find('assets/Title.png') ,
            size_hint = (0.85, 0.85),
            allow_stretch = True,
            pos = (center_x, center_y)
        )
        
        layout.add_widget(self.title)
        self.title.bind(on_release = self.title_change_image)
        
        #title frog
        self.titlefrog = Image(
            source = resource_find('assets/TitleFrog.png') ,
            size_hint= (0.15, 0.15),
            pos = (Window.width, -50)
        )
        layout.add_widget(self.titlefrog)
        
        #start button
        img_width = Window.width * 0.3
        center_x = (Window.width - img_width) / 2
        center_y = Window.height * 0.05
        
        self.startbtn = ImageButton(
            source = resource_find('assets/StartButton.png') ,
            size_hint = (0.4, 0.4) ,
            pos = (img_width, center_y)
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
            self.title.source = resource_find('assets/Titleb.png')
        except Exception as e:
            log_error("title_chage_image", e)

    def start_jump_animation(self):
        try:
            anim = Animation(x=self.titlefrog.x - Window.width - 200, duration=4.5)
            anim.bind(on_complete=self.reset_position)
            anim.start(self.titlefrog)
        except Exception as e:
            log_error("start_jump_animation", e)

    def reset_position(self, *args):
        self.titlefrog.x = Window.width
        self.start_jump_animation()
        
    def go_to_game(self, *args):
        self.anim_btn = Animation(opacity = 0, duration = 0.2)
        self.anim_btn.bind(on_complete = lambda *_: self.contin())
        self.anim_btn.start(self.startbtn)
        
    def contin(self):
        try:
            self.manager.current = 'game'
        except Exception as e:
            log_error("StartScreen.contin", e)

    def on_enter(self):
        self.title_anim()

    def on_leave(self, *args):
        self.anim.stop(self.title)