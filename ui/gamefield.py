from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout


class GameField(GridLayout):
    cols = 5
    rows = 3


class BattleField(FloatLayout):

    def __init__(self, **kwargs):
        self.my_units = []
        self.enemy_units = []
        app = App.get_running_app()
        self.size_hint = (None, None)
        self.size = app.root.get_screen("gamefield").ids.gamefield.size
        self.pos = app.root.get_screen("gamefield").ids.gamefield.pos
        super(BattleField, self).__init__(**kwargs)





