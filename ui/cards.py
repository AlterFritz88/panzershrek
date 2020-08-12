from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.animation import Animation
from kivy.app import App


class BattleCard(ButtonBehavior, Image):

    def __init__(self, field_pos, **kwargs):
        self.field_pos = field_pos
        super(BattleCard, self).__init__(**kwargs)

    def select(self):
        app = App.get_running_app()
        if not app.selected:
            app.selected = self
            self.source = 'icon.png'
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
            print(app.selected.id)
            app.root.get_screen("gamefield").ids.gamefield.units[0].source = 'test.png'

            animation = Animation(pos=self.pos)
            animation.start(app.selected)

            app.selected = None
