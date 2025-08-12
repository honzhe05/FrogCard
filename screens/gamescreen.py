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
from components.XPcircle import ExpArc
from logic.save_manager import save_game, load_game, clear_save
from screens.shop import ShopPanel
from screens.startscreen import StartScreen

class GameScreen(Screen):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.menu_open = False
        
        self.shop_panel = ShopPanel()
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.fly_layer = FloatLayout()
        self.layout.add_widget(self.fly_layer)
        self.start_screen = StartScreen()
        
        #top bar
        topbar = Image(
            source = resource_find('assets/Topbar.png' ) ,
            size_hint = (None , None) ,
            allow_stretch = True ,
            keep_ratio = True
        )
        topbar.texture_update()
        img_w, img_h = topbar.texture.size
        screen_w, screen_h = Window.size
        topbar.width = screen_w
        topbar.height = screen_w * img_h / img_w
        
        topbar.pos = (0 , screen_h - topbar.height)
        self.layout.add_widget(topbar)
        
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
        
        # money and diamond
        self.money = self.create_label(str(self.app.mn), {'x': 0.8, 'y': 0.949})
        self.diamond = self.create_label(str(self.app.dm), {'x': 0.4, 'y': 0.948})
        self.layout.add_widget(self.money)
        self.layout.add_widget(self.diamond)
        
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
            
        #menu button
        self.menu_button = ImageButton(
            source = resource_find('assets/Menu.png'),
            size_hint = (None , None) ,
            size = (100 , 80),
            allow_stretch = True ,
            keep_ratio = True ,
            pos_hint = {'x' : 0.9 , 'y' : 0.895}
        )
        self.layout.add_widget(self.menu_button)
        self.menu_button.bind(on_release = self.open_menu)
        
        #garbage button
        self.garbage = ImageButton(
            source = os.path.join('assets' , 'Garbage.png') ,
            size_hint = (None , None) ,
            allow_stretch = True ,
            keep_ratio = True ,
            pos_hint = {'x' : 0.9 , 'y' : 0.85}
        )
        self.garbage.bind(on_release = self.gb_clear)
        self.layout.add_widget(self.garbage)
        self.garbage.opacity = 0
        self.garbage.disabled = True
        
        #exp bar
        size_bar = 200
        self.exp_bar = ExpArc(
            size_hint = (None , None),
            size=(size_bar*2, size_bar*2),
            pos=(-size_bar, Window.height - size_bar)
        )
        self.layout.add_widget(self.exp_bar)
        self.create_exp_level_label()
        self.load()
        
    def hide_flies(self):
            self.fly_layer.opacity = 0

    def show_flies(self):
        self.fly_layer.opacity = 1
        
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
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[GameScreen.spawn_flies] {e}\n")
                
    #money hint
    def money_hint(self , money):
        money_label = Label(
            text = str(money) ,
            font_name = 'NotoSans-Regular' ,
            size_hint=(None, None),
            size=(100, 80),
            pos=(
                Window.width*0.82 ,
                Window.height*0.85
            ) ,
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
            )
        self.layout.add_widget(money_label)
            
        anim_mn = Animation(y=money_label.y + 180 ,  opacity=0 , duration = 0.7)
        anim_mn.bind(on_complete=lambda *args: self.layout.remove_widget(money_label))
        anim_mn.start(money_label)
                
    def create_exp_level_label(self):
        if hasattr(self, 'exp_level') and self.exp_level.parent:
            self.layout.remove_widget(self.exp_level)
        
        self.exp_level = Label(
            text=str(self.exp_bar.level),
            font_name='NotoSans-Light',
            size_hint=(None, None),
            font_size= 90,
            pos_hint={'x': 0.03 , 'y': 0.941},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.layout.add_widget(self.exp_level)
    
    def update_exp_level_label(self):
        self.exp_level.text = str(self.exp_bar.level)
            
    def create_label(self, text, pos_hint):
            return Label(
                text=text,
                font_name = 'NotoSans-Regular' ,
                size_hint=(None, None),
                size=(100, 50),
                pos_hint=pos_hint,
                halign="center",
                valign="middle",
                color=(1, 1, 1, 1),
                outline_color=(0, 0, 0, 1),
                outline_width=2
            )
            
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
    
    def open_menu(self, button):
        self.menu_open = not self.menu_open
        if self.menu_open:
            button.source = resource_find('assets/Menu2.png')
            self.garbage.opacity = 1
            self.garbage.disabled = False
        else:
            button.source = resource_find('assets/Menu.png')
            self.garbage.opacity = 0
            self.garbage.disabled = True
    
    def open_shop(self, *args):
        self.manager.current = 'shop'
       
    def save(self):
        try:
            save_game(
                self.app.mn,
                self.app.dm,
                self.exp_bar.current_exp,
                self.exp_bar.level,
                self.app.quan,
                self.app.quan_level,
                self.app.quan_mn
            )
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[GameScreen.save] {e}\n")
    
    def load(self):
        try:
            data = load_game()
            if data:
                self.app.mn = data.get("money", 100)
                self.app.dm = data.get("diamond", 10)
                self.exp_bar.current_exp = data.get("exp", 0)
                self.exp_bar.level = data.get("level", 1)
                self.app.quan = data.get("quan", 5)
                self.app.quan_level = data.get("quan_level", 1)
                self.app.quan_mn = data.get("quan_mn", 50)
                self.exp_bar.update_arc()
                self.create_exp_level_label()
    
                self.money.text = str(self.app.mn)
                self.diamond.text = str(self.app.dm)
                self.shop_panel.fly_quan.text = str(self.app.quan)
                self.spawn_flies(self.app.quan)
                self.shop_panel.quan_level_label.text = "LV. " + str(self.app.quan_level)
                self.shop_panel.quan_need_mn.text = str(self.app.quan_mn)
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[GameScreen.load] {e}\n")
            
    def clear_saved(self, *args):
        clear_save()
        self.load()