#shop.py
from kivy.app import App
from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from utils.error_handler import log_error
from components.statusbar import StatusBar

class DecorateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.status_bar = StatusBar(game_screen=self)
        self.status_bar.top_bar()
        self.add_widget(self.status_bar)
           
        bg = Image(
            source=resource_find('assets/DecorateShop.png'),
            size_hint=(None, None),
            size = Window.size,
            pos=(0, 0),
            allow_stretch=True
        )
        self.add_widget(bg)
        
        close_btn = Button(
            text='關閉', 
            font_name = 'NotoSans-Regular',
            size_hint=(None , None), 
            size = (180, 100),
            color=(0, 0, 0, 1),  
            background_normal = ' ' ,
            background_color = (0.265, 0.44, 0.108, 1),
            pos=(Window.width - 180, 
                Window.height *0.688
            )
        )
        self.add_widget(close_btn)
        close_btn.bind(on_release=self.hide)
        
        self.grass_mn = 100
        self.grass_btn = Button(
            text = '購買',
            font_name = 'NotoSans-Regular',
            size_hint=(None , None), 
            size = (170, 90),
            color=(0, 0, 0, 1),  
            background_normal = ' ' ,
            background_color = (0.265, 0.44, 0.108, 1),
            pos_hint = {'x': 0.73 , 'y': 0.61},
            disabled = True
        )
        self.add_widget(self.grass_btn)
        self.grass_btn.bind(on_release=self.buy_grass)
        
    def on_enter(self):
        if self.app.level >= 5 and self.app.buy_grass:
            self.grass_btn.disabled = False
        Clock.schedule_once(lambda dt: self.status_bar.exp_bar.update_arc(), 0)
        
    def hide(self, *args): 
        self.manager.current = 'game'
        
    def buy_grass(self, *args):
        try:
            if self.app.mn >= self.grass_mn:
                self.app.mn -= self.grass_mn
                game_screen = self.app.root.get_screen('game')
                shop_panel = self.app.root.get_screen('shop')
                decorate_screen = self.app.root.get_screen('decorate')
                game_screen.status_bar.money.text = str(self.app.mn)
                shop_panel.status_bar.money.text = str(self.app.mn)
                decorate_screen.status_bar.money.text = str(self.app.mn)
                
                self.status_bar.money_hint("-100")
                self.grass_btn.disabled = True
                self.app.buy_grass = False
                game_screen.load_decorate()
        except Exception as e:
            log_error("ShopPanel.buy_grass", e)