import os
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager , Screen , FadeTransition
from screens.startscreen import StartScreen
from screens.gamescreen import GameScreen
from screens.cardgallery import CardGalleryScreen

LabelBase.register(name="NotoSans-Regular",
    fn_regular=os.path.join("fonts", "NotoSansTC-Regular.ttf"))
LabelBase.register(name="NotoSans-Bold",
    fn_regular=os.path.join("fonts", "NotoSansTC-Bold.ttf"))
LabelBase.register(name="NotoSans-Light",
    fn_regular=os.path.join("fonts", "NotoSansTC-Light.ttf"))
Window.clearcolor = (0.66 , 0.36 , 0.17 , 1)
        
class MyApp(App):
    def build(self):
        self.mn = 100
        self.dm = 10
        self.quan = 5
        self.quan_level = 1
        self.quan_mn = 50
        
        #test
        #Window.size = (1080, 2000)
        
        sm = ScreenManager(transition=FadeTransition(duration = 0.5 , clearcolor = (0.66 , 0.36 , 0.17 , 1)))
        sm.add_widget(StartScreen(name= 'start'))
        sm.add_widget(GameScreen(name= 'game'))
        sm.add_widget(CardGalleryScreen(name='card'))
        return sm
        
    def on_stop(self):
        try:
            game_screen = self.root.get_screen('game')
            if hasattr(game_screen, 'save'):
                game_screen.save()
        except Exception as e:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"[on_stop] {e}\n")
     
if __name__ == '__main__' :
    MyApp().run()