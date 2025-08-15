import webbrowser
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.resources import resource_find
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from screens.startscreen import StartScreen
from screens.gamescreen import GameScreen
from screens.cardgallery import CardGalleryScreen
from screens.shop import ShopPanel
from screens.decoratescreen import DecorateScreen
from utils.error_handler import log_error
from update_checker import check_update
from config import APP_VERSION

update_info = check_update(APP_VERSION)

def show_update_popup(data):
    layout = BoxLayout(
        orientation='vertical',
        spacing=10,
        padding=10
    )
    label = Label(
        text=f"有新版本 {data['version']} ！",
        font_name="NotoSans-Regular",
    )
    update_btn_layout = BoxLayout(
            size_hint_y=None,
            height='40dp',
            spacing=10
        )
    down_btn = Button(
        text="前往下載",
        font_name="NotoSans-Regular",
        background_color=(0.444, 0.64, 0.736, 1),
        size_hint=(0.5, 0.8)
    )
    btn = Button(
        text="稍後下載",
        font_name="NotoSans-Regular",
        background_color=(0.444, 0.64, 0.736, 1),
        size_hint=(0.5, 0.8)
    )
    web_btn = Button(
        text="更新內容",
        font_name="NotoSans-Regular",
        background_color=(0.444, 0.64, 0.736, 1),
        size_hint=(0.5, 0.8)
    )
    layout.add_widget(label)
    
    update_btn_layout.add_widget(web_btn)
    update_btn_layout.add_widget(btn)
    update_btn_layout.add_widget(down_btn)
    layout.add_widget(update_btn_layout)
    
    popup = Popup(
        title="Update Notification!!",
        background=' ',
        background_color=(0.444, 0.64, 0.736, 1),
        content=layout,
        size_hint=(0.7, 0.23),
        auto_dismiss=False
    )
    down_btn.bind(on_release=lambda *args: webbrowser.open(data["apk_url"]))
    btn.bind(on_release=popup.dismiss)
    web_btn.bind(on_release=lambda *args: webbrowser.open(data["html_url"]))
    popup.open()

try:
    LabelBase.register(
        name="NotoSans-Regular",
        fn_regular=resource_find("fonts/NotoSansTC-Regular.ttf")
    )
    LabelBase.register(
        name="NotoSans-Bold",
        fn_regular=resource_find("fonts/NotoSansTC-Bold.ttf")
    )
    LabelBase.register(
        name="NotoSans-Light",
        fn_regular=resource_find("fonts/NotoSansTC-Light.ttf")
    )
except Exception as e:
    log_error("LabelBase.Register", e)
        
def safe_set_clearcolor(first_try=True):
    try:
        Window.clearcolor = (0.66, 0.36, 0.17, 1)
    except Exception as e:
        if first_try:
            Clock.schedule_once(lambda dt: safe_set_clearcolor(False), 0.5)
        else:
            log_error("Window_color_setting", e)

safe_set_clearcolor()

class MyApp(App):
    def build(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        except:
            pass
        
        self.skip_save_on_exit = False
        self.mn = 100
        self.dm = 10
        self.quan = 5
        self.quan_level = 1
        self.quan_mn = 50
        self.exp = 0
        self.level = 1
        self.max_exp = 100
        self.buy_grass = True
        self.buy_more_grass = True
        
        #test
        #Window.size = (1080, 2000)
        sm = ScreenManager(transition=FadeTransition(duration=0.5, clearcolor=(0.66 , 0.36 , 0.17 , 1)))
        self.game_screen = GameScreen(name='game')
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(self.game_screen)
        sm.add_widget(CardGalleryScreen(name='card'))
        sm.add_widget(ShopPanel(name='shop'))
        sm.add_widget(DecorateScreen(name='decorate'))
        Window.bind(on_key_down=self.on_key)
        try:
            Clock.schedule_interval(self.game_screen.save, 360)
        except Exception as e:
            log_error("auto_save", e)
        return sm
        
    def on_start(self):
        Clock.schedule_once(self.check_for_update, 1)

    def check_for_update(self, dt):
        update_info = check_update(APP_VERSION)
        if update_info:
            show_update_popup(update_info)
        
    def on_stop(self):
        if self.skip_save_on_exit:
            return
        try:
            self.game_screen.save(0)
        except Exception as e:
            log_error("on_stop", e)
    
    def on_pause(self):
        if self.skip_save_on_exit:
            return
        try:
            self.game_screen.save(0)
            return True
        except Exception as e:
            log_error("on_pause", e)
            return True
                
    def on_key(self, window, key, *args):
        if key==27:
            sm = self.root
            try:
                if sm.current != 'game' and sm.current != 'start':
                    sm.current = 'game'
                else:
                    self.show_exit_popup()
                return True
            except Exception as e:
                log_error("go_to_game.screen", e)
                return True
        return False
         
    def show_exit_popup(self):
        layout = BoxLayout(
            orientation='vertical',
            padding=0,
            spacing=10,
        )
        label = Label(
            text= '你真的想要退出嗎？(盯',
            font_name = 'NotoSans-Regular'
        )
        btn_layout = BoxLayout(
            size_hint_y=None,
            height='40dp',
            spacing=10,
        )

        btn_yes = Button(
            text='Yes',
            size_hint=(0.5, 0.8),
            background_color=(0.544, 0.74, 0.836, 1)
        )
        btn_no = Button(
            text='No',
            size_hint=(0.5, 0.8),
            background_color=(0.544, 0.74, 0.836, 1)
        )

        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)

        layout.add_widget(label)
        layout.add_widget(btn_layout)

        popup = Popup(
            title='Are You Sure?',
            content=layout,
            background=' ',
            background_color=(0.444, 0.64, 0.736, 1),
            size_hint=(0.65, 0.2),
            auto_dismiss=False,
        )

        btn_yes.bind(on_release=self.stop_app)
        btn_yes.bind(on_release=popup.dismiss)
        btn_no.bind(on_release=popup.dismiss)

        popup.open()

    def stop_app(self, *args):
        self.stop()

if __name__ == '__main__':
    MyApp().run()
