#cardgallery.py
import json
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

class CardGalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(CardGallery())

class CardGallery(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 外層：一欄式排版（每個分類佔一行）
        outer = GridLayout(cols=1, spacing=20, padding=10, size_hint_y=None)
        outer.bind(minimum_height=outer.setter('height'))

        with open('data/cardinfo.json', encoding='utf-8') as f:
            all_cards = json.load(f)

        for rarity, cards in all_cards.items():
            # 標題：佔一整行
            title = Label(
                text=rarity,
                font_name='NotoSans-Light',
                size_hint_y=None,
                height=100
            )
            outer.add_widget(title)

            # 卡片區：三欄排版
            grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
            grid.bind(minimum_height=grid.setter('height'))

            for card in cards:
                btn = Button(
                    text=card['name'],
                    font_name='NotoSans-Light',
                    size_hint_y=None,
                    height=200
                )
                grid.add_widget(btn)

            outer.add_widget(grid)

        self.add_widget(outer)