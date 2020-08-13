from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.animation import Animation
from kivy.app import App


class BattleCard(ButtonBehavior, Image):

    def __init__(self, field_pos, my_unit, **kwargs):
        self.field_pos = field_pos
        self.my_unit = my_unit
        super(BattleCard, self).__init__(**kwargs)

    def select(self):
        app = App.get_running_app()
        if self.my_unit:
            if not app.selected:
                app.selected = {'item': self, 'num': app.root.get_screen("gamefield").ids.gamefield.my_units.index(self)}
                self.source = 'icon.png'
                app.root.get_screen("gamefield").ids.gamefield.remove_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.add_widget(self)
            else:
                app.selected = None
                self.source = 'test.png'


class EmptyField(Button):

    def __init__(self, field_pos, **kwargs):
        self.field_pos = field_pos
        super(EmptyField, self).__init__(**kwargs)

    def move(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].source = 'test.png'

            animation = Animation(pos=self.pos)
            animation.start(app.selected['item'])

            app.selected = None
