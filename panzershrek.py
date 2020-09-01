from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock


class PanzerShrek(MDApp):
    selected = None
    moving = False
    card_in_reserve = None
    occupied_cells = []

    def build(self):

        return Builder.load_file('ui/main_ui.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = 'Green'

    def on_start(self):
        Clock.schedule_once(lambda *args: self.prepear_field())

    def prepear_field(self):
        self.root.get_screen("gamefield").ids.gamefield.new_game()

if __name__ == '__main__':

    Window.size = (1920//1.5, 1080//1.5)
    PanzerShrek().run()