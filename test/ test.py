from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale
from kivy.animation import Animation
from kivy.core.window import Window
from math import cos, radians


class FlipCardWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        self.rotation_active = True

        start_y = -500
        target_y = Window.height / 2 - 250
        center_x = Window.width / 2 - 250

        self.card_front = Image(
            source='assets/TitleFrog.png',
            size_hint=(None, None),
            size=(500, 500),
            pos=(center_x, start_y),
            opacity=0
        )
        self.card_back = Image(
            source='assets/back.png',
            size_hint=(None, None),
            size=(500, 500),
            pos=(center_x, start_y),
            opacity=0
        )

        self.add_widget(self.card_back)
        self.add_widget(self.card_front)

        for img in [self.card_front, self.card_back]:
            with img.canvas.before:
                PushMatrix()
                rot = Rotate(angle=self.angle, axis=(
                    0, 0, 1), origin=img.center)
                scale = Scale(x=1, y=1, z=1, origin=img.center)
            with img.canvas.after:
                PopMatrix()
            img._rot = rot
            img._scale = scale

        move_anim = Animation(y=target_y, duration=1.2, t='out_back')
        rotate_anim = Animation(angle=360, duration=1.2, t='linear')
        rotate_anim.bind(on_progress=self.update_rotation)
        rotate_anim.bind(on_complete=self.finalize_card)

        move_anim.start(self.card_front)
        move_anim.start(self.card_back)
        rotate_anim.start(self)

    def update_rotation(self, anim, widget, progress):
        if not self.rotation_active:
            return

        self.angle = self.angle % 360
        rad = radians(self.angle)
        scale_x = max(abs(cos(rad)), 0.05)

        for img in [self.card_front, self.card_back]:
            img._rot.angle = self.angle
            img._rot.origin = img.center
            img._scale.origin = img.center

        self.card_front._scale.x = scale_x
        self.card_back._scale.x = 1 - scale_x

        self.card_front.opacity = cos(rad)
        self.card_back.opacity = 1 - cos(rad)

    def finalize_card(self, *args):
        self.rotation_active = False

        # 穩定定格：角色圖與背景圖都展開且完全顯示
        self.card_front.opacity = 1
        self.card_front._scale.x = 1

        self.card_back.opacity = 1
        self.card_back._scale.x = 1  # ✅ 這一行是關鍵


class FlipCardApp(App):
    def build(self):
        return FlipCardWidget()


if __name__ == '__main__':
    FlipCardApp().run()
