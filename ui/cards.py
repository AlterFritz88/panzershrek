from itertools import product, starmap
import math

from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Color, Line, Rectangle, Rotate, PopMatrix, PushMatrix


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

        if not self.my_unit and not app.moving and app.selected:
            cells = list(starmap(lambda a, b: (self.field_pos[0] + a, self.field_pos[1] + b), product((0, -1, +1), (0, -1, +1))))[1:]

            myradians = math.atan2(self.pos[1] - app.selected['item'].pos[1], self.pos[0] - app.selected['item'].pos[0])
            angle = math.degrees(myradians)
            print(self.pos, app.selected['item'].pos)
            self.BANG = Bang(source='imgs/bullet.png', pos=app.selected['item'].pos, size=self.size,
                             size_hint=(None, None), angle=angle,)

            app.root.get_screen("gamefield").ids.gamefield.add_widget(self.BANG)
            animation = Animation(pos=self.pos)
            animation.start(self.BANG)

            if app.selected['item'].field_pos in cells:     # если карта соседняя, то атакую
                self.attack()

        if self.my_unit and not app.moving:
            clear_green_blank_cell()
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
                self.border_line = Line(width=3, rectangle=[self.x, self.y, self.width, self.height])
                self.canvas.add(self.border_line)

    def attack(self):
        pass


class BattleCardReserve(ButtonBehavior, Image, BoxLayout):
    def selected(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].canvas.remove(
                app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].border_line)
            app.selected = {}

        if self.parent.children.index(self) != app.card_in_reserve and not app.moving:
            clear_green_blank_cell()
            if app.card_in_reserve is not None:
                self.parent.children[app.card_in_reserve].pos[1] -= 50
            self.pos[1] = self.pos[1] + 50
            app.card_in_reserve = self.parent.children.index(self)

            draw_widget = [x for x in app.root.get_screen("gamefield").ids.gamefield.children if str(type(x)) == "<class 'ui.cards.EmptyField'>" and x.field_pos in ((0,1), (1,1), (1,0))]
            for wid in draw_widget:
                color = Color(0.1, 0.7, 0.3, 0.15)
                rect = Rectangle(pos=wid.pos, size=(wid.width, wid.width))
                wid.canvas.add(color)
                wid.canvas.add(rect)
                wid.draw_obj = [color, rect]
        else:
            if app.card_in_reserve is not None:
                clear_green_blank_cell()
                self.pos[1] = self.pos[1] - 50
                app.card_in_reserve = None


def clear_green_blank_cell():
    app = App.get_running_app()
    draw_widget = [x for x in app.root.get_screen("gamefield").ids.gamefield.children if
                   str(type(x)) == "<class 'ui.cards.EmptyField'>" and x.field_pos in ((0, 1), (1, 1), (1, 0))]
    for wid in draw_widget:
        for obj in wid.draw_obj:
            wid.canvas.remove(obj)
        wid.draw_obj = []


class EmptyField(Button):

    def __init__(self, field_pos, **kwargs):
        self.field_pos = field_pos
        self.draw_obj = []
        super(EmptyField, self).__init__(**kwargs)

    def move(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].canvas.remove(app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].border_line)
            app.occupied_cells.remove(app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].field_pos)
            app.root.get_screen("gamefield").ids.gamefield.my_units[app.selected['num']].field_pos = self.field_pos
            app.occupied_cells.append(self.field_pos)
            self.BANG = Image(source='imgs/bang.gif', pos=self.pos, size=self.size, size_hint=(None, None), anim_delay=0,
                         anim_loop=1)
            app.root.get_screen("gamefield").ids.gamefield.add_widget(self.BANG)
            animation = Animation(pos=self.pos)
            app.moving = True
            animation.bind(on_complete=self.unblock)
            animation.start(app.selected['item'])
            app.selected = None
            return

        if app.card_in_reserve is not None and self.field_pos in ((0, 1), (1, 1), (1, 0)):
            pos_x = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[0] + app.card_size
            pos_y = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[1]
            unit = BattleCard(source='imgs/stab1.png', pos=(pos_x, pos_y),
                                        size=(app.card_size, app.card_size),
                                        size_hint=(None, None), field_pos=self.field_pos, my_unit=True)
            app.root.get_screen("gamefield").ids.gamefield.my_units.append(unit)
            app.root.get_screen("gamefield").ids.gamefield.add_widget(unit)
            app.root.get_screen("gamefield").ids.gamefield.my_units.append(unit)
            app.occupied_cells.append(self.field_pos)
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
        app.root.get_screen("gamefield").ids.gamefield.remove_widget(self.BANG)


class Bang(Image):
    def __init__(self, angle, **kwargs):

        super(Bang, self).__init__(**kwargs)
        self.rotate = Rotate(angle=angle)
        self.rotate.origin = self.center
        self.canvas.before.add(PushMatrix())
        self.canvas.before.add(self.rotate)
        self.canvas.after.add(PopMatrix())

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)

    def update_canvas(self, *args):
        self.rotate.origin = self.center