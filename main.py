# main.py
import platform
import config
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.startscreen import StartScreen
from screens.gamescreen import GameScreen
from screens.cardgallery import CardGalleryScreen
from screens.shop import ShopPanel
from screens.decoratescreen import DecorateScreen
from utils.error_handler import log_error
from update_checker import check_update
from config import APP_VERSION
from ui.fonts import register_fonts
from ui.update_popup import show_update_popup
from logic.bgm_player import MusicPlayer
from components.statusbar import StatusBar


def safe_set_clearcolor(first_try=True):
    try:
        Window.clearcolor = (0.66, 0.36, 0.17, 1)
    except Exception as e:
        if first_try:
            Clock.schedule_once(lambda dt: safe_set_clearcolor(False), 0.2)
        else:
            log_error("Window_color_setting", e)


safe_set_clearcolor()


class MyApp(App):
    def build(self):
        register_fonts()
        self.root = BoxLayout()
        self.loading_label = Label(
            text="載入中...",
            font_name='FCSSM',
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        self.root.add_widget(self.loading_label)
        Clock.schedule_once(self.load_screen, 1.5)
        Clock.schedule_once(self.init_main_ui, 1)
        return self.root

    def init_main_ui(self, dt=None):
        self.skip_save_on_exit = False
        self.mn = 100
        self.dm = 10
        self.quan = 5
        self.quan_level = 1
        self.quan_mn = 50
        self.xp = 2
        self.xp_level = 1
        self.xp_mn = 100
        self.exp = 0
        self.level = 1
        self.max_exp = 100
        self.buy_grass = True
        self.buy_more_grass = True
        self.buy_cloud = True
        self.buy_tree = True
        self.buy_apple = True
        self.con = False
        self.music = 100
        self.sound = 100
        self.h = 0
        self.m = 0
        self.s = 0
        self.music_now = "None"
        self.is_exiting = True

        # test
        # Window.size = (720, 1520)

        self.sm = ScreenManager(
            transition=FadeTransition(
                duration=0.5,
                clearcolor=(0.66, 0.36, 0.17, 1)
            )
        )
        self.game_screen = GameScreen(name='game')
        self.sm.add_widget(StartScreen(name='start'))
        self.sm.add_widget(GameScreen(name='game'))

        self.root.clear_widgets()
        self.root.add_widget(self.sm)

    def load_screen(self, dt=None):
        Clock.schedule_once(
            lambda dt: self.sm.add_widget(DecorateScreen(name='decorate')),
            0.5
        )
        Clock.schedule_once(
            lambda dt: self.sm.add_widget(CardGalleryScreen(name='card')),
            2
        )
        Clock.schedule_once(
            lambda dt: self.sm.add_widget(ShopPanel(name='shop')),
            3.5
        )
        try:
            Clock.schedule_once(
                lambda dt: Clock.schedule_interval(self.game_screen.save, 300),
                10
            )
        except Exception as e:
            log_error("auto_save", e)

    def on_start(self):
        Clock.schedule_once(self.check_update, 4)
        Clock.schedule_once(self.play_music, 6.5)
        Clock.schedule_once(
            lambda dt:
            Window.bind(on_key_down=self.on_key),
            2
        )

    def play_music(self, dt):
        bgms = [
            ("IfIHadaChicken", 150, "If I Had a Chicken"),
            ("JauntyGumption", 118, "Jaunty Gumption"),
            ("TheBuilder", 117, "The Builder"),
            ("HiddenAgenda", 135, "Hidden Agenda"),
            ("Wallpaper", 220, "Wallpaper"),
        ]
        try:
            self.statusbar = StatusBar()
            self.player = MusicPlayer(bgms, self.statusbar)
            self.player.play_next()
        except Exception as e:
            log_error("play_music", e)

    def get_screen(self, name):
        return self.sm.get_screen(name)

    def check_update(self, dt):
        arch = platform.machine()
        if "aarch64" in arch:
            config.ABI = "arm64-v8a"
        elif "arm" in arch:
            config.ABI = "armeabi-v7a"

        update_info = check_update(APP_VERSION)
        if update_info:
            show_update_popup(update_info)

    def on_stop(self):
        self.is_exiting = False
        self.stop_game("on_stop")

    def on_pause(self):
        self.stop_game("on_pause")

    def stop_game(self, source):
        if self.skip_save_on_exit:
            return
        try:
            self.game_screen.save()
            return True
        except Exception as e:
            log_error(source, e)
            return True

    def on_key(self, window, key, *args):
        if key == 27:
            if (
                self.con and
                hasattr(self, 'popup') and
                self.popup._window is not None and
                self.is_exiting
            ):
                self.popup.dismiss()
                self.con = False
                return True
            self.con = True

            try:
                if self.sm.current != 'game' and self.sm.current != 'start':
                    self.sm.current = 'game'
                else:
                    self.show_exit_popup()
                return True
            except Exception as e:
                log_error("go_to_game.screen", e)
                return True
        return False

    def show_exit_popup(self):
        layout = BoxLayout(
            orientation='vertical',
            padding=0,
            spacing=10
        )
        label = Label(
            text='你真的想要退出嗎？(盯',
            font_name='FCSSM'
        )
        btn_layout = BoxLayout(
            size_hint_y=None,
            height='40dp',
            spacing=10
        )

        btn_yes = self.btn_yn('yes')
        btn_no = self.btn_yn('no')

        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)

        layout.add_widget(label)
        layout.add_widget(btn_layout)

        self.popup = Popup(
            title='Are You Sure?',
            content=layout,
            background='',
            background_color=(0.444, 0.64, 0.736, 1),
            size_hint=(0.65, 0.2),
            auto_dismiss=False,
        )

        btn_yes.bind(
            on_release=lambda *args: self.popup.dismiss()
        )
        btn_yes.bind(on_release=self.stop_app)
        btn_no.bind(on_release=self.popup.dismiss)
        self.popup.open()

    def btn_yn(self, text):
        return Button(
            text=text,
            size_hint=(0.5, 0.8),
            background_color=(0.544, 0.74, 0.836, 1)
        )

    def stop_app(self, *args):
        self.stop()


if __name__ == '__main__':
    MyApp().run()
