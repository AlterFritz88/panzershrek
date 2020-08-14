from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window


class PanzerShrek(MDApp):
    selected = None
    moving = False
    def build(self):
        return Builder.load_file('ui/main_ui.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = 'Green'

    def on_start(self):
        self.root.get_screen("gamefield").ids.gamefield.update_canvas()
        #self.root.ids.my_widget.update_canvas()


if __name__ == '__main__':

    Window.size = (1920, 1080)
    PanzerShrek().run()