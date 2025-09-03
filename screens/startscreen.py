# startscreen.py
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_find
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from components.imagebutton import ImageButton
from utils.error_handler import log_error
from config import FULL_VERSION
from logic.bgm_player import MusicPlayer
from components.statusbar import StatusBar


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.app = App.get_running_app()

        # background
        background = Image(
            source=resource_find('assets/Background.png'),
            size_hint=(1, 1),
            pos=(0, 0),
            allow_stretch=True,
            keep_ratio=False
        )
        self.layout.add_widget(background)

        # version
        nm = round(dp(11))
        nnm = round(dp(10.5))
        version_text = Label(
            text=(
                f"[size={nm}]Game Version: {FULL_VERSION}\n"
                f"[size={nnm}]Did you know? "
                f"I created two new bugs while trying to fix one.\n"
                f"[size={nnm}]Spent over two hours tweaking and debugging... "
                f"still couldn't fix it.\n"
                f"[size={nnm}]Game Developer: "
                f"Honzhe, AvianJay and copilot. "
                f"wait nooo\n"
            ),
            markup=True,
            font_name='FCSSM',
            size_hint=(1, 1),
            font_size=nm,
            pos_hint={'x': 0.01, 'top': 0.997},
            halign='left',
            valign='top',
            color=(0.25, 0.35, 0, 1)
        )
        version_text.bind(size=version_text.setter('text_size'))
        self.layout.add_widget(version_text)

        # title
        img_width = Window.width * 0.85
        center_x = (Window.width - img_width) / 2
        center_y = Window.height * 0.22

        self.title = ImageButton(
            source=resource_find('assets/Title.png'),
            size_hint=(0.85, 0.85),
            allow_stretch=True,
            pos=(center_x, center_y)
        )

        self.layout.add_widget(self.title)
        self.title.bind(on_release=self.title_change_image)

        # title frog
        self.titlefrog = Image(
            source=resource_find('assets/TitleFrog.png'),
            size_hint=(0.15, 0.15),
            pos=(Window.width, -50)
        )
        self.layout.add_widget(self.titlefrog)

        # start button
        img_width = Window.width * 0.3
        center_x = (Window.width - img_width) / 2
        center_y = Window.height * 0.05

        self.startbtn = ImageButton(
            source=resource_find('assets/StartButton.png'),
            size_hint=(0.4, 0.4),
            pos=(img_width, center_y)
        )
        self.layout.add_widget(self.startbtn)
        self.startbtn.bind(on_release=self.go_to_game)

        Clock.schedule_once(self.add_start, 1)
        self.start_jump_animation()

    def add_start(self, dt):
        self.add_widget(self.layout)

    def title_anim(self):
        base_y = Window.height * 0.03
        offset = self.title.y
        self.anim_up = Animation(y=offset + base_y, duration=0.5)
        self.anim_down = Animation(y=offset, duration=0.8)
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
            anim = Animation(
                x=self.titlefrog.x - Window.width - 200,
                duration=4.5
            )
            anim.bind(on_complete=self.reset_position)
            anim.start(self.titlefrog)
        except Exception as e:
            log_error("start_jump_animation", e)

    def reset_position(self, *args):
        self.titlefrog.x = Window.width
        self.start_jump_animation()

    def go_to_game(self, *args):
        self.anim_btn = Animation(opacity=0, duration=0.2)
        self.anim_btn.bind(on_complete=lambda *_: self.contin())
        self.anim_btn.start(self.startbtn)
            
    def play_music(self, stop=False):
        if stop:
            if hasattr(self, 'player'):
                self.player.stop_play()
            return
    
        if not hasattr(self, 'statusbar'):
            self.statusbar = StatusBar()
    
        bgms = [
            ("IfIHadaChicken", 63, "If I Had a Chicken"),
            ("JauntyGumption", 68, "Jaunty Gumption"),
            ("TheBuilder", 70, "The Builder"),
            ("HiddenAgenda", 60, "Hidden Agenda")
        ]
        if not hasattr(self, 'player'):
            self.player = MusicPlayer(bgms, self.statusbar)
    
        Clock.schedule_once(self.player.play_next, 0.1)
    
    def contin(self):
        try:
            self.manager.current = 'game'
        except Exception as e:
            log_error("StartScreen.contin", e)

    def on_enter(self):
        self.title_anim()
        self.play_music()

    def on_leave(self, *args):
        self.anim.stop(self.title)
