# imagebutton.py
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

class ImageButton(ButtonBehavior , Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mipmap = True