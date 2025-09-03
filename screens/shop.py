# shop.py
from kivy.app import App
from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from components.statusbar import StatusBar
from utils.error_handler import log_error


class ShopPanel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.status_bar = StatusBar()

        bg = Image(
            source=resource_find('assets/Shop.png'),
            size_hint=(None, None),
            size=Window.size,
            pos=(0, 0)
        )
        self.add_widget(bg)

        self.status_bar.top_bar()
        self.add_widget(self.status_bar)

        self.fly_quan = Label(
            text=str(self.app.quan),
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=60,
            pos_hint={'x': 0.56, 'y': 0.508},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.add_widget(self.fly_quan)

        self.xp_quan = Label(
            text=str(self.app.xp),
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=60,
            pos_hint={'x': 0.56, 'y': 0.408},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.add_widget(self.xp_quan)

        self.quan_level_label = Label(
            text=f"LV. {self.app.quan_level}",
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=40,
            pos_hint={'x': 0.26, 'y': 0.538},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.add_widget(self.quan_level_label)

        self.xp_level_label = Label(
            text=f"LV. {self.app.xp_level}",
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=40,
            pos_hint={'x': 0.26, 'y': 0.438},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.add_widget(self.xp_level_label)

        self.quan_need_mn = Label(
            text=str(self.app.quan_mn),
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=50,
            pos_hint={'x': 0.82, 'y': 0.508},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
        )
        self.add_widget(self.quan_need_mn)

        self.xp_btn = Button(
            text='購買',
            font_name='FCSSM',
            size_hint=(None, None),
            size=(160, 100),
            color=(0, 0, 0, 1),
            background_normal='',
            background_color=(0.265, 0.44, 0.108, 1),
            pos_hint={'x': 0.65, 'y': 0.408},
        )
        self.add_widget(self.xp_btn)
        self.xp_btn.bind(on_release=self.buy_xp)
        if self.app.xp_level >= 5:
            self.xp_btn.disabled = True
            self.app.xp_mn = "MAX"

        self.xp_need_mn = Label(
            text=str(self.app.xp_mn),
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=50,
            pos_hint={'x': 0.82, 'y': 0.408},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
        )
        self.add_widget(self.xp_need_mn)

        quan_btn = Button(
            text='購買',
            font_name='FCSSM',
            size_hint=(None, None),
            size=(160, 100),
            color=(0, 0, 0, 1),
            background_normal='',
            background_color=(0.265, 0.44, 0.108, 1),
            pos_hint={'x': 0.65, 'y': 0.508}
        )
        self.add_widget(quan_btn)
        quan_btn.bind(on_release=self.buy_quan)

        close_btn = Button(
            text='X',
            font_name='FCSSM',
            size_hint=(None, None),
            font_size=55,
            size=(100, 90),
            color=(0.065, 0.24, 0, 1),
            background_normal='',
            background_color=(0.265, 0.44, 0.108, 1),
            pos=(
                Window.width - 100,
                Window.height * 0.591,
            ),
        )
        self.add_widget(close_btn)
        close_btn.bind(on_release=self.hide)

    def on_enter(self):
        self.game_screen = self.app.sm.get_screen('game')
        Clock.schedule_once(lambda dt: self.status_bar.exp_bar.update_arc(), 0)
        self.update_label()

        if self.game_screen:
            self.game_screen.hide_flies()

    def on_leave(self):
        if self.game_screen:
            self.game_screen.show_flies()

    def hide(self, *args):
        self.manager.current = 'game'

    def update_label(self):
        self.fly_quan.text = str(self.app.quan)
        self.xp_quan.text = str(self.app.xp)
        self.xp_level_label.text = f"LV. {self.app.xp_level}"
        self.quan_level_label.text = f"LV. {self.app.quan_level}"
        self.xp_need_mn.text = str(self.app.xp_mn)
        self.quan_need_mn.text = str(self.app.quan_mn)
        self.status_bar.money.text = str(self.app.mn)
        self.status_bar.update_exp_level_label()

    def buy_xp(self, *args):
        try:
            if self.app.mn >= self.app.xp_mn:
                self.app.mn -= self.app.xp_mn
                self.decorate_screen = self.app.sm.get_screen('decorate')
                self.status_bar.money.text = str(self.app.mn)
                self.game_screen.status_bar.money.text = str(self.app.mn)
                self.decorate_screen.status_bar.money.text = str(self.app.mn)
                self.status_bar.money_hint("-" + str(self.app.xp_mn))
                self.app.xp_level += 1

                self.app.xp_mn = (
                    100 +
                    (50 * int(self.app.xp_level)) *
                    (int(self.app.xp_level) - 1)
                )
                self.app.xp = int(self.app.xp * 1.5)
                self.update_xp(self.app.xp)

        except Exception as e:
            log_error("ShopPanel.buy_xp", e)

    def buy_quan(self, *args):
        try:
            if self.app.mn >= self.app.quan_mn:
                self.app.mn -= self.app.quan_mn
                self.decorate_screen = self.app.sm.get_screen('decorate')
                self.status_bar.money.text = str(self.app.mn)
                self.game_screen.status_bar.money.text = str(self.app.mn)
                self.decorate_screen.status_bar.money.text = str(self.app.mn)
                self.status_bar.money_hint("-" + str(self.app.quan_mn))
                self.app.quan_level += 1
                self.app.quan_mn = 50 + \
                    ((10 * int(self.app.quan_level))
                     * (int(self.app.quan_level) - 1))
                self.app.quan += 1
                self.update_quan(self.app.quan)
                self.game_screen.spawn_flies(1)
        except Exception as e:
            log_error("ShopPanel.buy_quan", e)

    def update_quan(self, new_value):
        self.app.quan = new_value
        self.fly_quan.text = str(self.app.quan)
        self.quan_level_label.text = "LV. " + str(self.app.quan_level)
        self.quan_need_mn.text = str(self.app.quan_mn)

    def update_xp(self, new_value):
        self.app.xp = new_value
        self.xp_quan.text = str(self.app.xp)
        self.xp_level_label.text = "LV. " + str(self.app.xp_level)
        self.xp_need_mn.text = str(self.app.xp_mn)
        if self.app.xp_level >= 5:
            self.xp_btn.disabled = True
            self.xp_need_mn.text = "MAX"
