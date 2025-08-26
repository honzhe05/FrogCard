# update_popup.py
import webbrowser
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


def show_update_popup(data):
    layout = BoxLayout(
        orientation='vertical',
        spacing=0,
        padding=10
    )
    label = Label(
        text=f"有新版本 {data['version']} ！",
        font_name="FCSSM",
    )
    update_btn_layout = BoxLayout(
        size_hint_y=None,
        height='40dp',
        spacing=10
    )
    down_btn = Button(
        text="前往下載",
        font_name="FCSSM",
        background_color=(0.444, 0.64, 0.736, 1),
        size_hint=(0.5, 0.8)
    )
    btn = Button(
        text="稍後下載",
        font_name="FCSSM",
        background_color=(0.444, 0.64, 0.736, 1),
        size_hint=(0.5, 0.8)
    )
    web_btn = Button(
        text="更新內容",
        font_name="FCSSM",
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
        background='',
        background_color=(0.444, 0.64, 0.736, 1),
        content=layout,
        size_hint=(0.7, 0.23),
        auto_dismiss=False
    )
    down_btn.bind(on_release=lambda *args: webbrowser.open(data["apk_url"]))
    btn.bind(on_release=popup.dismiss)
    web_btn.bind(on_release=lambda *args: webbrowser.open(data["html_url"]))
    popup.open()
