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
            self.border_color = (0, 0.8, 0.5, 0.5)
        else:
            self.border_color = (0.8, 0, 0.2, 0.5)
        super(BattleCard, self).__init__(**kwargs)

    #obj = ()

    def select(self):
        app = App.get_running_app()
        if self.my_unit and not app.moving:
            if not app.selected:
                app.root.get_screen("gamefield").ids.gamefield.remove_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.add_widget(self)
                self.border_line = Line(width=3, rectangle=[self.x, self.y, self.width, self.height], )
                self.canvas.add(self.border_line)
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").ids.gamefield.my_units.index(self)}

                unit3 = BattleCard(source='test.jpg', size=(app.card_size, app.card_size),
                                   size_hint=(None, None), field_pos=(0, 0), my_unit=True)
                app.root.get_screen("gamefield").ids.reserve_cards.add_widget(unit3)

            else:
                app.root.get_screen("gamefield").ids.gamefield.remove_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.add_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].canvas.remove(app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].border_line)
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").ids.gamefield.my_units.index(self)}
                self.border_line = Line(width=3, rectangle=[self.x, self.y, self.width, self.height], )
                self.canvas.add(self.border_line)


class EmptyField(Button):

    def __init__(self, field_pos, **kwargs):
        self.field_pos = field_pos
        super(EmptyField, self).__init__(**kwargs)

    def move(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].source = 'test.jpg'
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].canvas.remove(app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].border_line)
            animation = Animation(pos=self.pos)
            app.moving = True
            animation.bind(on_complete=self.unblock)
            animation.start(app.selected['item'])
            app.selected = None

    def unblock(self, *args):
        app = App.get_running_app()
        app.moving = False