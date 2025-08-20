# fonts.py
from utils.error_handler import log_error
from kivy.core.text import LabelBase
from kivy.resources import resource_find


def register_fonts():
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
