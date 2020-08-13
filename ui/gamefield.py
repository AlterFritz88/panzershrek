import weakref
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

from .cards import BattleCard, EmptyField

class GameField(FloatLayout):

    # def __init__(self, **kwargs):
    #     self.update_canvas()
    #     super(GameField, self).__init__(**kwargs)

    def update_canvas(self):
        app = App.get_running_app()
        # the height of the cell is the height of the widget over the size of the grid rounded down (// takes only the integer bit)
        cellheight = app.root.height // 4.5
        # cellwidth is the same as height for this implementation but could be changed to different if you want
        cellwidth = cellheight
        app.card_size = cellheight
        print(app.root.size[0] // 10)
        start = app.root.size[0] // 6
        # start the circles from the point 0,0
        x = start
        y = app.root.size[1] // 5

        # wipe the canvas clean
        self.canvas.clear()
        app.grids_pos = {}

        # for r in range(3):
        # # loop through the rows
        #     for c in range(5):
        #         # loop through the columns
        #         # if the cell in the GRID is alive the circle should be green
        #
        #         Color(0.5, 0.5, 0.5, 0.5)
        #         # draw a circle
        #         app.grids_pos[(r, c)] = (x, y)
        #         Button(pos=(x, y), size=(cellwidth - 2, cellheight - 2), size_hint=(None, None))
        #         # add the width to go to the next position to draw the next circle
        #         x += cellwidth
        #     # go to the next row
        #     y += cellheight
        #     # and set the x value back to the beginning
        #     x = start

        with self.canvas:
            # in the canvas
            for r in range(3):
                # loop through the rows
                for c in range(5):
                    # loop through the columns
                    # if the cell in the GRID is alive the circle should be green

                    Color(0.5, 0.5, 0.5, 0.5)
                    # draw a circle
                    app.grids_pos[(r, c)] = (x, y)

                    self.add_widget(EmptyField(pos=(x, y), size=(cellwidth - 2, cellheight - 2), size_hint=(None, None),
                                               field_pos=(r, c)))
                    # add the width to go to the next position to draw the next circle
                    x += cellwidth
                # go to the next row
                y += cellheight
                # and set the x value back to the beginning
                x = start
        self.my_units = []
        self.enemy_units = []
        headquarter_my = BattleCard(source='test.jpg', pos=app.grids_pos[(0, 0)], size=(cellwidth - 2, cellheight - 2),
                       size_hint=(None, None), field_pos=(0, 0), my_unit=True)
        self.my_units.append(headquarter_my)
        self.add_widget(headquarter_my)
        headquarter_enemy = BattleCard(source='test.jpg', pos=app.grids_pos[(2, 4)], size=(cellwidth - 2, cellheight - 2),
                       size_hint=(None, None), field_pos=(2, 4), my_unit=True)
        self.add_widget(headquarter_enemy)
        self.my_units.append(headquarter_enemy)




