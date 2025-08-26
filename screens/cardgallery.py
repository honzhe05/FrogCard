# cardgallery.py
import json
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from utils.error_handler import log_error


class CardGalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()
        self.gallery = CardGallery()
        layout.add_widget(self.gallery)

        self.back_btn = Button(
            text="X",
            size_hint=(None, None),
            font_size=70,
            color=(0.56, 0.26, 0.07, 1),
            pos_hint={'top': 0.99, 'right': 0.98},
            background_normal='',
            background_color=(1, 1, 1, 0),
        )
        layout.add_widget(self.back_btn)
        self.back_btn.bind(on_release=self.close)

        self.add_widget(layout)

        self.gallery.bind(scroll_y=self.on_scroll)

    def on_scroll(self, instance, value):
        target_opacity = 1.0 if value >= 0.9 else 0.0
        Animation(opacity=target_opacity, duration=0.2).start(self.back_btn)
        if self.back_btn.opacity <= 0.3:
            self.back_btn.disabled = True
        else:
            self.back_btn.disabled = False

    def close(self, *args):
        self.manager.current = 'game'


class CardGallery(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        outer = GridLayout(cols=1, spacing=20, padding=10, size_hint_y=None)
        outer.bind(minimum_height=outer.setter('height'))

        try:
            with open('data/cardinfo.json', encoding='utf-8') as f:
                all_cards = json.load(f)
        except Exception as e:
            log_error("get_card_info_json", e)
            all_cards = {}

        for rarity, cards in all_cards.items():
            title = Label(
                text=rarity,
                font_name='FCSSM',
                size_hint_y=None,
                height=100,
            )
            outer.add_widget(title)

            grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
            grid.bind(minimum_height=grid.setter('height'))

            try:
                for card in cards:
                    btn = Button(
                        text=card['name'],
                        font_name='FCSSM',
                        size_hint_y=None,
                        height=200,
                    )
                    grid.add_widget(btn)

                outer.add_widget(grid)
            except Exception as e:
                log_error("add_card_button", e)

        self.add_widget(outer)
