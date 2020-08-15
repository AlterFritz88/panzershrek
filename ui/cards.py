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

    def select(self):
        app = App.get_running_app()
        if app.card_in_reserve is not None:
            app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[1] -= 50
            app.card_in_reserve = None

        if self.my_unit and not app.moving:
            if not app.selected:
                app.root.get_screen("gamefield").ids.gamefield.remove_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.add_widget(self)
                self.border_line = Line(width=3, rectangle=[self.x, self.y, self.width, self.height], )
                self.canvas.add(self.border_line)
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").ids.gamefield.my_units.index(self)}

                # добавляю карту в руку
                temp_data = app.root.get_screen("gamefield").ids.reserve_cards.data[::]
                temp_data += [{"source": 'imgs/stab1.png'}]
                app.root.get_screen("gamefield").ids.reserve_cards.data = temp_data
                app.root.get_screen("gamefield").ids.reserve_cards.refresh_from_data()

            else:
                app.root.get_screen("gamefield").ids.gamefield.remove_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.add_widget(self)
                app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].canvas.remove(app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].border_line)
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").ids.gamefield.my_units.index(self)}
                self.border_line = Line(width=3, rectangle=[self.x, self.y, self.width, self.height], )
                self.canvas.add(self.border_line)



class BattleCardReserve(ButtonBehavior, Image, BoxLayout):
    def selected(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].canvas.remove(
                app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].border_line)
            app.selected = {}

        if self.parent.children.index(self) != app.card_in_reserve and not app.moving:
            if app.card_in_reserve is not None:
                self.parent.children[app.card_in_reserve].pos[1] -= 50
            self.pos[1] = self.pos[1] + 50
            app.card_in_reserve = self.parent.children.index(self)
        else:
            if app.card_in_reserve is not None:
                self.pos[1] = self.pos[1] - 50
                app.card_in_reserve = None


class EmptyField(Button):

    def __init__(self, field_pos, **kwargs):
        self.field_pos = field_pos
        super(EmptyField, self).__init__(**kwargs)

    def move(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].canvas.remove(app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].border_line)
            animation = Animation(pos=self.pos)
            app.moving = True
            animation.bind(on_complete=self.unblock)
            animation.start(app.selected['item'])
            app.selected = None
            return
        if app.card_in_reserve is not None:
            pos_x = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[0] + app.card_size
            pos_y = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[1]
            unit = BattleCard(source='imgs/stab1.png', pos=(pos_x, pos_y),
                                        size=(app.card_size, app.card_size),
                                        size_hint=(None, None), field_pos=(0, 0), my_unit=True)
            app.root.get_screen("gamefield").ids.gamefield.my_units.append(unit)
            app.root.get_screen("gamefield").ids.gamefield.add_widget(unit)
            animation = Animation(pos=self.pos)
            app.moving = True
            animation.bind(on_complete=self.unblock)
            animation.start(unit)
            app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.remove_widget(app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve])
            app.root.get_screen("gamefield").ids.reserve_cards.data.remove({"source": 'imgs/stab1.png'})
            app.root.get_screen("gamefield").ids.reserve_cards.refresh_from_data()
            app.card_in_reserve = None

    def unblock(self, *args):
        app = App.get_running_app()
        app.moving = False