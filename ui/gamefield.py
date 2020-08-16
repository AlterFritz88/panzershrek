import weakref
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

from .cards import BattleCard, EmptyField


class GameField(FloatLayout):

    def update_canvas(self):
        app = App.get_running_app()

        cellheight = app.root.height // 4.5
        cellwidth = cellheight
        app.card_size = cellheight
        start = app.root.size[0] // 5
        x = start
        y = app.root.size[1] // 3.5
        self.canvas.clear()
        app.grids_pos = {}

        with self.canvas:
            # in the canvas
            for r in range(3):
                # loop through the rows
                for c in range(5):

                    Color(0.5, 0.5, 0.5, 0.5)
                    app.grids_pos[(r, c)] = (x, y)

                    self.add_widget(EmptyField(pos=(x, y), size=(cellwidth - 2, cellheight - 2), size_hint=(None, None),
                                               field_pos=(r, c)))
                    x += cellwidth
                # go to the next row
                y += cellheight
                # and set the x value back to the beginning
                x = start
        self.my_units = []
        self.enemy_units = []
        headquarter_my = BattleCard(source='imgs/stab1.png', pos=app.grids_pos[(0, 0)], size=(cellwidth - 2, cellheight - 2),
                       size_hint=(None, None), field_pos=(0, 0), my_unit=True)
        self.my_units.append(headquarter_my)
        self.add_widget(headquarter_my)
        headquarter_enemy = BattleCard(source='imgs/stab1.png', pos=app.grids_pos[(2, 4)], size=(cellwidth - 2, cellheight - 2),
                       size_hint=(None, None), field_pos=(2, 4), my_unit=False)
        self.add_widget(headquarter_enemy)
        self.my_units.append(headquarter_enemy)

        # unit = BattleCard(source='imgs/stab1.png', size=(cellwidth - 2, cellheight - 2),
        #                 size_hint=(None, None), field_pos=(0, 0), my_unit=True)
        # app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.add_widget(unit)
        app.occupied_cells.append((2, 4))
        app.occupied_cells.append((0, 0))




