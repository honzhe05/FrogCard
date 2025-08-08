from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager , Screen , NoTransition

LabelBase.register(name='MyFont' , fn_regular = 'NotoSansTC-VariableFont_wght.ttf')
Window.clearcolor = (0.66 , 0.36 , 0.17 , 0.6)

class ImageButton(ButtonBehavior , Image):
    pass

class StartScreen(Screen):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        background = Image(
            source = 'Background.jpg' ,
            size_hint = (1 , 1) ,
            pos = (0 , 0) ,
            allow_stretch = True ,
            keep_ratio = False
        )
        layout.add_widget(background)
        
        self.title = ImageButton(
            source = 'Title.png' ,
            size_hint = (None , None) ,
            size = (1000 , 1000) ,
            pos = (
                (Window.width - 1000) / 2 , 
                (Window.height - 850) * 0.75
            ) ,
            allow_stretch = True ,
            keep_ratio = True
        )
        self.anim_up = Animation(y = self.title.y + 50 , duration = 0.5)
        self.anim_down = Animation(y = self.title.y , duration = 0.8)
        self.anim = self.anim_up + self.anim_down
        self.anim.repeat = True
        self.anim.start(self.title)  
        
        self.title.bind(on_release = self.change_image)
        layout.add_widget(self.title)
        
        self.titlefrog = Image(
            source = 'titlefrog.png' ,
            size_hint = (None, None),
            size = (200 , 200) ,
            pos = (Window.width , 0) ,
            allow_stretch = True ,
            keep_ratio = True
        )
        layout.add_widget(self.titlefrog)
        
        self.startbtn = ImageButton(
            source = 'StartButton.png' ,
            size_hint = (None , None) ,
            size = (500 , 500) ,
            pos = (
                (Window.width - 500) / 2 , 
                (Window.height - 1000) * 0.25
            ) ,
            allow_stretch = True ,
            keep_ratio = True
        )
        layout.add_widget(self.startbtn)
        
        self.startbtn.bind(on_release = self.go_to_game)
        
    
        self.add_widget (layout)
        self.jump_distance = Window.width + 200
        self.jump_duration = 4.5
        
        self.start_jump_animation()
        
    def change_image(self ,  *args):
        self.anim.stop(self.title)
        self.title.source = 'Titleb.png' 

    def start_jump_animation(self):
        anim = Animation(x=self.titlefrog.x - self.jump_distance, duration=self.jump_duration)
        anim.bind(on_complete=self.reset_position)
        anim.start(self.titlefrog)

    def reset_position(self, *args):
        self.titlefrog.x = Window.width
        self.start_jump_animation()
        
    def go_to_game(self, *args):
        new_width = self.startbtn.width * 0.85
        new_height = self.startbtn.height * 0.85
        new_x = self.startbtn.x + (self.startbtn.width - new_width) / 2
        new_y = self.startbtn.y + (self.startbtn.height - new_height) / 2

        self.startbtn.size = (new_width, new_height)
        self.startbtn.pos = (new_x, new_y)
        self.manager.current = 'game'
        
class GameScreen(Screen):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.add_widget(layout)
        
        topbar = Image(
            source = 'Topbar.png' ,
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
        layout.add_widget(topbar)
        
        layout.add_widget(
            Label(
                text = ' 空空如也\n¯⁠\⁠_⁠(⁠ツ⁠)⁠_⁠/⁠¯' ,
                font_name = 'MyFont' ,
                font_size = 100
            )
        )
    
class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(StartScreen(name= 'start'))
        sm.add_widget(GameScreen(name= 'game'))
        return sm
        
MyApp().run()