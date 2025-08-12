import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from components.XPcircle import ExpArc

class ShopPanel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
       
        bg = Image(
            source=resource_find('assets/Shop.png'),
            size_hint=(None, None),
            size = Window.size,
            pos=(0, 0),
            allow_stretch=True
        )
        self.add_widget(bg)
        
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
        self.add_widget(topbar)
        
        self.money = self.create_label(str(self.app.mn), {'x': 0.8, 'y': 0.949})
        self.diamond = self.create_label(str(self.app.dm), {'x': 0.4, 'y': 0.948})
        self.add_widget(self.money)
        self.add_widget(self.diamond)
        
        self.fly_quan = Label(
            text = str(self.app.quan),
            font_name = 'NotoSans-Regular',
            size_hint=(None , None), 
            font_size = 60,
            pos_hint = {'x' : 0.56, 'y' : 0.508},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.add_widget(self.fly_quan)
        
        self.quan_level_label = Label(
            text = "LV. " + str(self.app.quan_level),
            font_name = 'NotoSans-Light',
            size_hint=(None , None), 
            font_size = 40,
            pos_hint = {'x' : 0.26, 'y' : 0.538},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.add_widget(self.quan_level_label)
        
        self.quan_need_mn = Label(
            text = str(self.app.quan_mn),
            font_name = 'NotoSans-Light',
            size_hint=(None , None), 
            font_size = 50,
            pos_hint = {'x' : 0.82, 'y' : 0.508},
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2
        )
        self.add_widget(self.quan_need_mn)
        
        quan_btn = Button(
            text = '購買',
            font_name = 'NotoSans-Regular',
            size_hint=(None , None), 
            size = (180, 100),
            color=(0, 0, 0, 1),  
            background_normal = ' ' ,
            background_color = (0.265, 0.44, 0.108, 1),
            pos_hint = {'x': 0.65 , 'y': 0.508}
        )
        self.add_widget(quan_btn)
        quan_btn.bind(on_release=self.buy_quan)
        
        close_btn = Button(
            text='關閉', 
            font_name = 'NotoSans-Regular',
            size_hint=(None , None), 
            size = (180, 100),
            color=(0, 0, 0, 1),  
            background_normal = ' ' ,
            background_color = (0.265, 0.44, 0.108, 1),
            pos=(Window.width - 180, 
                Window.height *0.591
            )
        )
        self.add_widget(close_btn)
        close_btn.bind(on_release=self.hide)
    
    def on_enter(self):
        self.game_screen = App.get_running_app().root.get_screen('game')
        if self.game_screen:
            self.game_screen.hide_flies()

    def on_leave(self):
        if self.game_screen:
            self.game_screen.show_flies()
    
    def hide(self, *args): 
        self.manager.current = 'game'
    
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
        
    def buy_quan(self, *args):
        try:
            if self.app.mn >= self.app.quan_mn:
                self.app.mn -= self.app.quan_mn
                self.game_screen.money.text = str(self.app.mn)
                self.money.text = str(self.app.mn)
                self.app.quan_level += 1
                self.app.quan_mn += 20 * (self.app.quan_level - 1)
                self.app.quan += 1
                self.update_quan(self.app.quan)
                self.game_screen.spawn_flies(1)
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[ShopPanel.buy_quan] {e}\n")

    def update_quan(self, new_value):
        self.app.quan = new_value
        self.fly_quan.text = str(self.app.quan)
        self.quan_level_label.text = "LV. " + str(self.app.quan_level)
        self.quan_need_mn.text = str(self.app.quan_mn)    