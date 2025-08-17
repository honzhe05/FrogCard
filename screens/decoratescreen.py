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
            pos=(0, 0)
        )
        self.add_widget(bg)
        
        close_btn = Button(
            text='X', 
            font_name = 'NotoSans-Regular',
            size_hint=(None , None), 
            font_size = 55,
            size = (100, 90),
            color=(0.065, 0.24, 0, 1),
            background_normal = '' ,
            background_color = (0.265, 0.44, 0.108, 1),
            pos=(Window.width - 100, 
                Window.height *0.688
            )
        )
        self.add_widget(close_btn)
        close_btn.bind(on_release=self.hide)
        
        self.grass_mn = 100
        self.grass_btn = self.create_btn({'x': 0.73 , 'y': 0.61})
        self.more_grass_mn = 200
        self.more_grass_btn = self.create_btn({'x': 0.73 , 'y': 0.51})
        self.cloud_mn = 300
        self.cloud_btn = self.create_btn({'x': 0.73 , 'y': 0.41})
        self.tree_mn = 500
        self.tree_btn = self.create_btn({'x': 0.73 , 'y': 0.305})
        self.apple_mn = 500
        self.apple_btn = self.create_btn({'x': 0.73 , 'y': 0.205})
        
        self.add_widget(self.grass_btn)
        self.add_widget(self.more_grass_btn)
        self.add_widget(self.cloud_btn)
        self.add_widget(self.tree_btn)
        self.add_widget(self.apple_btn)
        self.grass_btn.bind(on_release=self.buy_grass)
        self.more_grass_btn.bind(on_release=self.buy_more_grass)
        self.cloud_btn.bind(on_release=self.buy_cloud)
        self.tree_btn.bind(on_release=self.buy_tree)
        self.tree_btn.bind(on_release=self.buy_tree)
        self.apple_btn.bind(on_release=self.buy_apple)
        
    def create_btn(self, pos_hint):
        return Button(
            text = '購買',
            font_name = 'NotoSans-Regular',
            size_hint=(None , None), 
            size = (160, 90),
            color=(0, 0, 0, 1),  
            background_normal = '' ,
            background_color = (0.265, 0.44, 0.108, 1),
            pos_hint = pos_hint,
            disabled = True
        )
        
    def on_enter(self):
        if self.app.level >= 5 and self.app.buy_grass:
            self.grass_btn.disabled = False
        if self.app.level >= 15 and self.app.buy_more_grass:
            self.more_grass_btn.disabled = False
        if self.app.level >= 25 and self.app.buy_cloud:
            self.cloud_btn.disabled = False
        if self.app.level >= 40 and self.app.buy_tree:
            self.tree_btn.disabled = False
        if self.app.level >= 50 and self.app.buy_apple:
            self.apple_btn.disabled = False
                
        Clock.schedule_once(lambda dt: self.status_bar.exp_bar.update_arc(), 0)
        
    def hide(self, *args): 
        self.manager.current = 'game'
        
    def buy_grass(self, *args):
        try:
            if self.app.mn >= self.grass_mn:
                self.app.mn -= self.grass_mn
                self.deco_update_mn()
                
                self.status_bar.money_hint("-100")
                self.grass_btn.disabled = True
                self.app.buy_grass = False
                self.game_screen.load_decorate()
        except Exception as e:
            log_error("ShopPanel.buy_grass", e)
            
    def buy_more_grass(self, *args):
        try:
            if self.app.mn >= self.more_grass_mn:
                self.app.mn -= self.more_grass_mn
                self.deco_update_mn()
                
                self.status_bar.money_hint("-200")
                self.more_grass_btn.disabled = True
                self.app.buy_more_grass = False
                self.game_screen.load_decorate()
        except Exception as e:
            log_error("ShopPanel.buy_more_grass", e)
            
    def buy_cloud(self, *args):
        try:
            if self.app.mn >= self.cloud_mn:
                self.app.mn -= self.cloud_mn
                self.deco_update_mn()
                
                self.status_bar.money_hint("-300")
                self.cloud_btn.disabled = True
                self.app.buy_cloud = False
                self.game_screen.load_decorate()
        except Exception as e:
            log_error("ShopPanel.buy_cloud", e)
            
    def buy_tree(self, *args):
        try:
            if self.app.mn >= self.tree_mn:
                self.app.mn -= self.tree_mn
                self.deco_update_mn()
                
                self.status_bar.money_hint("-500")
                self.tree_btn.disabled = True
                self.app.buy_tree = False
                self.game_screen.load_decorate()
        except Exception as e:
            log_error("ShopPanel.buy_tree", e)
            
    def buy_apple(self, *args):
        try:
            if self.app.mn >= self.apple_mn:
                self.app.mn -= self.apple_mn
                self.deco_update_mn()
                
                self.status_bar.money_hint("-1000")
                self.apple_btn.disabled = True
                self.app.buy_apple = False
                self.game_screen.load_decorate()
        except Exception as e:
            log_error("ShopPanel.buy_apple", e)
            
    def deco_update_mn(self):
        try:
            self.game_screen = self.app.root.get_screen('game')
            shop_panel = self.app.root.get_screen('shop')
            decorate_screen = self.app.root.get_screen('decorate')
            self.game_screen.status_bar.money.text = str(self.app.mn)
            shop_panel.status_bar.money.text = str(self.app.mn)
            decorate_screen.status_bar.money.text = str(self.app.mn)
        except Exception as e:
            log_error("deco_update_mn")