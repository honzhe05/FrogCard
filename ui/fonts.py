# fonts.py
from utils.error_handler import log_error
from kivy.core.text import LabelBase
from kivy.resources import resource_find


def register_fonts():
    try:
        LabelBase.register(
            name="FCSSM",
            fn_regular=resource_find("fonts/FrogCardSubsetM.otf")
        )
        LabelBase.register(
            name="FCSSB",
            fn_regular=resource_find("fonts/FrogCardSubsetB.otf")
        )
    except Exception as e:
        log_error("LabelBase.Register", e)
