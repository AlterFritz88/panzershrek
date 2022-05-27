from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

from .units import LehrStab


# class GameField(FloatLayout):
#
#     def update_canvas(self):
#         app = App.get_running_app()
#
#         cellheight = app.root.height // 4.5
#         cellwidth = cellheight
#         app.card_size = cellheight
#         start = app.root.size[0] // 5
#         x = start
#         y = app.root.size[1] // 3.5
#         self.canvas.clear()
#         app.grids_pos = {}
#
#         with self.canvas:
#             # in the canvas
#             for r in range(3):
#                 # loop through the rows
#                 for c in range(5):
#
#                     Color(0.5, 0.5, 0.5, 0.5)
#                     app.grids_pos[(r, c)] = (x, y)
#
#                     self.add_widget(EmptyField(pos=(x, y), size=(cellwidth - 2, cellheight - 2), size_hint=(None, None),
#                                                field_pos=(r, c)))
#                     x += cellwidth
#                 # go to the next row
#                 y += cellheight
#                 # and set the x value back to the beginning
#                 x = start


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



