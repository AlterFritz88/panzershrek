from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Color, Line


class BattleCard(ButtonBehavior, Image, BoxLayout):

    def __init__(self, field_pos, my_unit, **kwargs):
        self.field_pos = field_pos
        self.my_unit = my_unit
        if self.my_unit:
            self.border_color = (0.9, 0.5, 0.5, 0.5)
        super(BattleCard, self).__init__(**kwargs)

            # with self.canvas.before:
            #     Color(rgba=(1, .5, .5, 1))
            #     Line(width=12, rectangle=[self.x, self.y, self.width, self.height], )

    def select(self):
        app = App.get_running_app()
        if self.my_unit:
            if not app.selected:
                app.root.get_screen("gamefield").ids.gamefield.remove_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.add_widget(self)
                self.source = 'icon.jpg'
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").ids.gamefield.my_units.index(self)}
            else:
                app.root.get_screen("gamefield").ids.gamefield.remove_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.add_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].source = 'test.jpg'
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").ids.gamefield.my_units.index(self)}
                self.source = 'icon.jpg'


class EmptyField(Button):

    def __init__(self, field_pos, **kwargs):
        self.field_pos = field_pos
        super(EmptyField, self).__init__(**kwargs)

    def move(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].source = 'test.jpg'

            animation = Animation(pos=self.pos)
            animation.start(app.selected['item'])

            app.selected = None
