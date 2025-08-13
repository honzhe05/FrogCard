from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.resources import resource_find
from components.XPcircle import ExpArc
from components.imagebutton import ImageButton
from kivy.graphics import PushMatrix, PopMatrix, Rotate

class StatusBar(FloatLayout):
    def __init__(self, game_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.app = App.get_running_app()
        self.menu_open = False
        
    def top_bar(self):
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
        
        # money and diamond
        self.money = self.create_label(str(self.app.mn), {'x': 0.8, 'y': 0.949})
        self.diamond = self.create_label(str(self.app.dm), {'x': 0.4, 'y': 0.948})
        self.layout.add_widget(self.money)
        self.layout.add_widget(self.diamond)
        
        size_bar = 200
        self.exp_bar = ExpArc(
            size_hint = (None , None),
            size=(size_bar*2, size_bar*2),
            pos=(-size_bar, Window.height - size_bar)
        )
        self.layout.add_widget(self.exp_bar)
        self.create_exp_level_label()
        
        self.menu_button = ImageButton(
            source = resource_find('assets/Menu.png'),
            size_hint = (None , None) ,
            size = (100 , 80),
            allow_stretch = True ,
            keep_ratio = True ,
            pos_hint = {'x' : 0.9 , 'y' : 0.895}
        )
        self.layout.add_widget(self.menu_button)
        self.menu_button.bind(on_release=self.open_menu)
        
        self.garbage = ImageButton(
            source = resource_find('assets/Garbage.png') ,
            size_hint = (None , None) ,
            allow_stretch = True ,
            keep_ratio = True ,
            pos_hint = {'x' : 0.9 , 'y' : 0.85}
        )
        self.garbage.bind(on_release=self._on_garbage)
        self.layout.add_widget(self.garbage)
        self.garbage.opacity = 0
        self.garbage.disabled = True
      
    def set_game_screen(self, game_screen):
        self.game_screen = game_screen
    
    def _on_garbage(self, *args):
        self.game_screen.gb_clear()   
        
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
        
    def money_hint(self, money):
        label = Label(
            text=str(money),
            font_name='NotoSans-Regular',
            font_size = 42,
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
        self.exp_level = Label(
            text=str(self.app.level),
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
        self.exp_level.text = str(self.app.level)
        
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