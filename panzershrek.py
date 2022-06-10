from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock
from connection_service import create_connection
from ui.gamefield import BattleField

from ui.game_session import GameSession


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
        create_connection()

    def on_start(self):
        self.root.get_screen("gamefield").add_widget(BattleField())
        self.card_size = self.root.get_screen("gamefield").ids["2,0"].width
        print(self.card_size)

    def start_new_game(self):
        self.root.current = "waiting_partner_screen"
        self.game_session = GameSession()
        self.game_session.give_me_a_partner()


if __name__ == '__main__':
    Window.size = (1920//2.5, 1080//2.5)
    PanzerShrek().run()