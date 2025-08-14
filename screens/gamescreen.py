#gamescreen.py
import random
import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.resources import resource_find
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from logic.fly import MovingFly
from components.imagebutton import ImageButton
from logic.save_manager import save_game, load_game, clear_save
from screens.shop import ShopPanel
from components.XPcircle import ExpArc
from screens.startscreen import StartScreen
from components.statusbar import StatusBar
from utils.error_handler import log_error
from screens.decoratescreen import DecorateScreen

class GameScreen(Screen):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
        self.shop_panel = ShopPanel()
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.fly_layer = FloatLayout()
        self.layout.add_widget(self.fly_layer)
        self.start_screen = StartScreen()
        self.status_bar = StatusBar(game_screen=self)
        self.status_bar.top_bar()
        self.add_widget(self.status_bar)
        
        self.status_bar.set_game_screen(self)
        
        #top bar
        self.status_bar.top_bar()
        
        # button bar
        buttonbar = Image(
            source = resource_find('assets/Buttonbar.png' ) ,
            size_hint = (None , None) ,
            allow_stretch = True ,
            keep_ratio = True ,
            pos = (0, 0)
        )
        buttonbar.texture_update()
        img_w, img_h = buttonbar.texture.size
        screen_w, screen_h = Window.size
        buttonbar.width = screen_w
        buttonbar.height = screen_w * img_h / img_w
        self.layout.add_widget(buttonbar)
        self.btn_h = buttonbar.height
        
        #shop menu
        self.shop_menu = ImageButton(
            source = resource_find('assets/Shopicon.png'),
            size_hint = (None , None),
            size = (200, 150),
            pos_hint = {'x': 0.04 , 'y' : 0.006}
        )
        self.layout.add_widget(self.shop_menu)
        self.shop_menu.bind(on_release = self.open_shop)
        
        #card menu
        self.cardmenu = ImageButton(
            source = resource_find('assets/CardShop.png'),
            size_hint = (None , None),
            size = (250, 150),
            pos_hint = {'x': 0.38 , 'y' : 0.006}
        )
        self.layout.add_widget(self.cardmenu)
        self.cardmenu.bind(on_release = self.open_card)
        
        #decorate menu
        self.decorate_menu = ImageButton(
            source = resource_find('assets/Tree.png'),
            size_hint = (None , None),
            size = (200, 150),
            pos_hint = {'x': 0.78 , 'y' : 0.006}
        )
        self.layout.add_widget(self.decorate_menu)
        self.decorate_menu.bind(on_release = self.open_decorate)
            
        self.load()
        self.load_decorate()
        
    def hide_flies(self):
            self.fly_layer.opacity = 0

    def show_flies(self):
        self.fly_layer.opacity = 1
        
    def load_decorate(self):
        if not self.app.buy_grass:
            grass_image = Image(
                source = resource_find('assets/Grass.png' ) ,
                size_hint = (0.25 , 0.15) ,
                allow_stretch = True ,
                keep_ratio = True ,
                pos = (Window.width * 0.4, 150)
            )
            self.layout.add_widget(grass_image)
        
    #fly
    def spawn_flies(self, count):
        try:
            for _ in range(count):
                random_size = random.randint(140, 160)
                fly = MovingFly(
                    source=resource_find('assets/Fly.png'),
                    size_hint=(None, None),
                    size=(random_size, random_size)
                )
                fly.pos = (
                    random.randint(0, Window.width - 100),
                    random.randint(200, Window.height - 300)
                )
                self.fly_layer.add_widget(fly)
        except Exception as e:
            log_error("GameScreen.spawn_flies", e)
                                     
    def open_card(self, *args):
        self.manager.current = 'card'
    
    def gb_clear(self , *args):
        self.confirm_del()
        
    def do_del(self , button_instance):
        self.layout.remove_widget(self.confirm_btn)
        self.layout.remove_widget(self.cancel_btn)
        self.layout.remove_widget(self.info_screen)
        
        clear_save()
        self.clear_label = Label(
            text = "資料將清除，並關閉遊戲" ,
            font_name = 'NotoSans-Bold' ,
            size_hint = (None , None) ,
            font_size = 60 ,
            pos_hint = {'x' : 0.45 , 'y' : 0.5} ,
            color=(1, 1, 1, 1),  
            outline_color=(0, 0, 0, 1),  
            outline_width=2
        )
        self.layout.add_widget(self.clear_label)
        Clock.schedule_once(self.reset_game , 1.5)
        
    def not_del(self , button_instance):
        self.layout.remove_widget(self.confirm_btn)
        self.layout.remove_widget(self.cancel_btn)
        self.layout.remove_widget(self.info_screen)
        
    def confirm_del(self, *args):
        confirm_btn = Button(
            text = "確認" ,
            font_name = 'NotoSans-Regular' ,
            size_hint = (None , None),
            size = (200, 100),
            pos = (
                Window.width / 2 + 5,
                Window.height * 0.4
            ),
            color=(0, 0, 0, 1),  
            background_normal = ' ' ,
            background_color = (0.96 , 0.96 , 0.86 , 1)
        )
        self.layout.add_widget(confirm_btn)
        
        cancel_btn = Button(
            text = "取消" ,
            font_name = 'NotoSans-Regular' ,
            size_hint = (None , None),
            size = (200, 100),
            pos = (
                Window.width / 2 - 205,
                Window.height * 0.4
            ),
            color=(0, 0, 0, 1),  
            background_normal = ' ' ,
            background_color = (0.96 , 0.96 , 0.86 , 1)
        )
        self.layout.add_widget(cancel_btn)
        
        info_screen = Button(
        text = "確定要刪除資料？" ,
            font_name = 'NotoSans-Regular' ,
            size_hint = (None , None),
            size = (410, 200),
            pos = (
                Window.width / 2 - 205,
                Window.height * 0.4 + 110
            ),
            disabled = True,
            opacity = 1,
            disabled_color=(0, 0, 0, 1),  
            background_disabled_normal = ' ' ,
            background_color = (0.96 , 0.96 , 0.86 , 1)
        )
        self.layout.add_widget(info_screen)
        
        self.confirm_btn = confirm_btn
        self.cancel_btn = cancel_btn
        self.info_screen = info_screen
        
        confirm_btn.bind(on_release=self.do_del)
        cancel_btn.bind(on_release=self.not_del)

    def reset_game(self, dt):
        app = App.get_running_app()
        app.skip_save_on_exit = True
        app.stop()
        
    def remove_all_flies(self):
        self.fly_layer.clear_widgets()
    
    def open_shop(self, *args):
        self.manager.current = 'shop'
        
    def open_decorate(self, *args):
       self.manager.current = 'decorate'
 
    def save(self, dt):
        try:
            save_game(
                self.app.mn,
                self.app.dm,
                self.app.exp,
                self.app.level,
                self.app.quan,
                self.app.quan_level,
                self.app.quan_mn,
                self.app.max_exp,
                self.app.buy_grass
            )
        except Exception as e:
            log_error(f"GameScreen.save", e)
    
    def load(self):
        try:
            data = load_game()
            if data:
                self.app.mn = data.get("money", 100)
                self.app.dm = data.get("diamond", 10)
                self.app.exp = data.get("exp", 0)
                self.app.level = data.get("level", 1)
                self.status_bar.exp_bar.level = self.app.level
                self.app.quan = data.get("quan", 5)
                self.app.quan_level = data.get("quan_level", 1)
                self.app.quan_mn = data.get("quan_mn", 50)
                self.app.exp_max = data.get("exp_max", 100)
                self.app.buy_grass = data.get("buy_grass", True)
                self.status_bar.exp_bar.update_arc()
                self.status_bar.create_exp_level_label()
                
                self.status_bar.money.text = str(self.app.mn)
                self.status_bar.diamond.text = str(self.app.dm)
                self.shop_panel.fly_quan.text = str(self.app.quan)
                self.spawn_flies(self.app.quan)
                self.shop_panel.quan_level_label.text = "LV. " + str(self.app.quan_level)
                self.shop_panel.quan_need_mn.text = str(self.app.quan_mn)
        except Exception as e:
            log_error(f"GameScreen.load", e)
            
    def clear_saved(self, *args):
        clear_save()
        self.load()