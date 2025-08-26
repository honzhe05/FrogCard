# statusbar.py
import webbrowser
from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.resources import resource_find
from kivy.uix.switch import Switch
from components.imagebutton import ImageButton
from utils.error_handler import log_error
from components.XPcircle import ExpArc
from config import FULL_VERSION_in_setting
from utils.playtimer import PlayTimer


class StatusBar(FloatLayout):
    def __init__(self, game_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.setting_layout = FloatLayout()
        self.app = App.get_running_app()
        self.timer = PlayTimer()
        self.menu_open = False
        self.top_bar()
        Clock.schedule_interval(
            self._sync_music_label,
            1
        )

    def top_bar(self):
        self.topbar = Image(
            source=resource_find('assets/Topbar.png'),
            size_hint=(None, None)
        )
        self.update_top_bar()

        # money and diamond
        if hasattr(self, 'money') and self.money.parent:
            self.layout.remove_widget(self.money)
        if hasattr(self, 'diamond') and self.diamond.parent:
            self.layout.remove_widget(self.diamond)

        self.money = self.create_label(
            str(self.app.mn), {'x': 0.8, 'y': 0.949})
        self.diamond = self.create_label(
            str(self.app.dm), {'x': 0.4, 'y': 0.949})
        self.layout.add_widget(self.money)
        self.layout.add_widget(self.diamond)

        # exp bar
        size_bar = dp(75)
        self.exp_bar = ExpArc(
            size_hint=(None, None),
            size=(size_bar*2, size_bar*2),
            pos=(-size_bar, Window.height - size_bar)
        )
        self.layout.add_widget(self.exp_bar)
        self.create_exp_level_label()

        # menu_button
        w = round(dp(37))
        h = round(dp(29.6))
        self.menu_button = ImageButton(
            source=resource_find('assets/Menu.png'),
            size_hint=(None, None),
            size=(w, h),
            pos_hint={'x': 0.9, 'y': 0.895},
        )
        self.layout.add_widget(self.menu_button)
        self.menu_button.bind(on_release=self.open_menu)

        # self.setting
        self.setting = ImageButton(
            source=resource_find('assets/Setting.png'),
            size_hint=(None, None),
            pos_hint={'x': 0.9, 'y': 0.85},
        )
        self.setting.bind(on_release=self._on_setting)
        self.layout.add_widget(self.setting)
        self.setting.opacity = 0
        self.setting.disabled = True

        # setting menu
        setting_menu = Image(
            source=resource_find('assets/SettingMenu.png'),
            size_hint=(0.9, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.setting_layout.add_widget(setting_menu)

        # self.garbage
        self.garbage = ImageButton(
            source=resource_find('assets/Garbage.png'),
            size_hint=(None, None),
            pos_hint={'x': 0.28, 'y': 0.32}
        )
        self.garbage.bind(on_release=self._on_garbage)
        self.setting_layout.add_widget(self.garbage)

        close_btn = Button(
            text='X',
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=55,
            size=(130, 90),
            color=(0.065, 0.24, 0, 1),
            background_normal='',
            background_color=(0.265, 0.44, 0.108, 1),
            pos=(
                Window.width - 350,
                Window.height * 0.7,
            ),
        )
        self.setting_layout.add_widget(close_btn)
        close_btn.bind(on_release=self.hide)

        # version text
        nm = round(dp(10))
        version_text = Label(
            text=str(FULL_VERSION_in_setting),
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=nm*1.1,
            halign='center',
            valign='middle',
            pos_hint={'x': 0.28, 'y': 0.397},
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.setting_layout.add_widget(version_text)

        # time label
        time_label = Label(
            text=self.timer.get_time_str(),
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=nm * 1.5,
            pos_hint={'x': 0.64, 'y': 0.4},
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.setting_layout.add_widget(time_label)
        Clock.schedule_interval(lambda dt: setattr(
            time_label, 'text', self.timer.get_time_str()), 1)

        # info
        self.info = Label(
            text="FrogCard – Play With Charm.",
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=nm * 1.3,
            pos_hint={'center_x': 0.5, 'y': 0.27},
            color=(0.365, 0.54, 0.208, 1)
        )
        self.setting_layout.add_widget(self.info)
        
        # guthub web
        self.github = ImageButton(
            source=resource_find('assets/Github.png'),
            size_hint=(None, None),
            pos_hint={'x': 0.73, 'y': 0.27}
        )
        self.setting_layout.add_widget(self.github)
        self.github.bind(on_release=self.open_github)

        # music label
        self.music_now = Label(
            text="None",
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=round(dp(10)) * 1.5,
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'y': 0.477},
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.setting_layout.add_widget(self.music_now)

        # music volume
        self.music_vol = Switch(
            active=True,
            size_hint=(None, None),
            size=(dp(220), dp(20)),
            pos_hint={'center_x': 0.53, 'y': 0.63}
        )
        self.setting_layout.add_widget(self.music_vol)
        self.music_vol.bind(active=self.on_switch)

    def on_switch(self, instance, value):
        if value:
            pass
        else:
            pass

    def show_music(self, song_name):
        self.music_now.text = song_name

    def _sync_music_label(self, dt):
        if self.setting_layout.parent:
            current_song = App.get_running_app().music_now
            if self.music_now.text != current_song:
                self.music_now.text = current_song

    def update_top_bar(self, dt=None):
        self.topbar.texture_update()
        img_w, img_h = self.topbar.texture.size
        screen_w, screen_h = Window.size
        self.topbar.width = screen_w
        self.topbar.height = screen_w * img_h / img_w
        self.topbar.pos = (0, screen_h - self.topbar.height)

        if self.topbar.parent:
            self.topbar.parent.remove_widget(self.topbar)
        self.layout.add_widget(self.topbar, index=6)

    def set_game_screen(self, game_screen):
        self.game_screen = game_screen

    def hide(self, *args):
        self.remove_widget(self.setting_layout)

    def open_github(self, *args):
        webbrowser.open("https://github.com/honzhe05/FrogCard")

    def _on_garbage(self, *args):
        try:
            self.remove_widget(self.setting_layout)
            self.game_screen.gb_clear()
        except Exception as e:
            log_error("_on_garbage_clear_save", e)

    def _on_setting(self, *args):
        try:
            self.show_music(App.get_running_app().music_now)
            self.add_widget(self.setting_layout)
        except Exception as e:
            log_error("_on_setting", e)

    def create_label(self, text, pos_hint):
        return Label(
            text=text,
            font_name='FCSSM',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint=pos_hint,
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )

    def money_hint(self, money):
        label = Label(
            text=str(money),
            font_name='FCSSM',
            font_size=round(dp(15.6)),
            bold=True,
            size_hint=(None, None),
            size=(120, 100),
            pos=(
                Window.width * 0.81,
                Window.height * 0.86
            ),
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
            opacity=1
        )
        self.layout.add_widget(label)

        move_anim = Animation(y=label.y + 100, opacity=0, duration=0.6)

        move_anim.bind(on_complete=lambda *a: self.layout.remove_widget(label))
        move_anim.start(label)

    def create_exp_level_label(self):
        if hasattr(self, 'exp_level') and self.exp_level.parent:
            self.layout.remove_widget(self.exp_level)
        self.exp_level = Label(
            text=str(self.app.level),
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=dp(33.3),
            pos_hint={'x': 0.03, 'y': 0.941},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.layout.add_widget(self.exp_level)

    def update_exp_level_label(self):
        self.exp_level.text = str(self.app.level)

    def open_menu(self, button):
        try:
            self.menu_open = not self.menu_open
            if self.menu_open:
                button.source = resource_find('assets/Menu2.png')
                self.setting.opacity = 1
                self.setting.disabled = False
            else:
                button.source = resource_find('assets/Menu.png')
                self.setting.opacity = 0
                self.setting.disabled = True
        except Exception as e:
            log_error("open_menu", e)
