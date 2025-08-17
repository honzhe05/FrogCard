#exit_popup.py
from kivy.uix.popup import Popup
from utils.error_handler import log_error
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

def show_exit_popup(q):
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

    self.popup = Popup(
        title='Are You Sure?',
        content=layout,
        background='',
        background_color=(0.444, 0.64, 0.736, 1),
        size_hint=(0.65, 0.2),
        auto_dismiss=False,
    )

    btn_yes.bind(on_release=self.stop_app)
    btn_yes.bind(on_release=self.popup.dismiss)
    btn_no.bind(on_release=self.popup.dismiss)

    self.popup.open()

def stop_app(self, *args):
    self.stop()
