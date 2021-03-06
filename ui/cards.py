from itertools import product, starmap
import importlib
import math

from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Color, Line, Rectangle, Rotate, PopMatrix, PushMatrix
from kivy.clock import Clock


class BattleCard(ButtonBehavior, Image, BoxLayout):

    def __init__(self, field_pos, my_unit, **kwargs):
        self.field_pos = field_pos
        self.my_unit = my_unit
        if self.my_unit:
            self.border_color = (0, 0.8, 0.5, 0.25)
        else:
            self.border_color = (0.8, 0, 0.2, 0.25)
        self.choose_color = (1, 1, 1, 0.0)
        super(BattleCard, self).__init__(**kwargs)

    def select(self):
        app = App.get_running_app()
        if app.card_in_reserve is not None:
            app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[1] -= 50
            app.card_in_reserve = None

        if not self.my_unit and not app.moving and app.selected:
            try:
                app.root.get_screen("gamefield").children[0].remove_widget(self.BANG)
            except AttributeError:
                pass

            cells = list(starmap(lambda a, b: (self.field_pos[0] + a, self.field_pos[1] + b), product((0, -1, +1), (0, -1, +1))))[1:]
            if app.selected['item'].field_pos in cells or app.selected['item'].type in ('stab', 'art'):     # если карта соседняя, то атакую
                self.attack()

        if self.my_unit and not app.moving:
            clear_green_blank_cell()
            if not app.selected:

                app.root.get_screen("gamefield").children[0].remove_widget(self)
                app.root.get_screen("gamefield").children[0].add_widget(self)
                self.canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.95)
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").children[0].my_units.index(self)}

                # добавляю карту в руку
                temp_data = app.root.get_screen("gamefield").ids.reserve_cards.data[::]
                temp_data += [{"card": 'LehrStab'}]
                app.root.get_screen("gamefield").ids.reserve_cards.data = temp_data
                app.root.get_screen("gamefield").ids.reserve_cards.refresh_from_data()

            else:
                app.root.get_screen("gamefield").children[0].remove_widget(self)
                app.root.get_screen("gamefield").children[0].add_widget(self)

                app.root.get_screen("gamefield").children[0].my_units[app.selected['num']].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").children[0].my_units.index(self)}
                self.canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.95)

    def attack(self):
        app = App.get_running_app()
        myradians = math.atan2(self.pos[1] - app.selected['item'].pos[1], self.pos[0] - app.selected['item'].pos[0])
        angle = math.degrees(myradians)
        self.BANG = Bang(source='imgs/bullet.png', pos=app.selected['item'].pos,
                         size=(self.size[0] // 2, self.size[1] // 2),
                         size_hint=(None, None), angle=angle, center_x=app.selected['item'].center_x,
                         center_y=app.selected['item'].center_y)

        app.root.get_screen("gamefield").children[0].add_widget(self.BANG)
        animation = Animation(pos=(self.pos[0] + self.size[1] // 4, self.pos[1] + self.size[1] // 4), d=0.2)
        animation.bind(on_complete=self._kill_bullet)
        animation.start(self.BANG)

    def _kill_bullet(self, *args):
        app = App.get_running_app()
        animation = Animation(pos=(self.pos[0] + 10, self.pos[1]), d=0.05)
        animation += Animation(pos=(self.pos[0] - 10, self.pos[1]), d=0.05)
        animation += Animation(pos=(self.pos[0], self.pos[1]), d=0.1)
        animation.start(self)
        app.root.get_screen("gamefield").children[0].remove_widget(self.BANG)
        self.BANG = Image(source='imgs/bang.gif', pos=self.pos, size=self.size, size_hint=(None, None), anim_delay=0,
                          anim_loop=1)
        app.root.get_screen("gamefield").children[0].add_widget(self.BANG)
        self.health -= app.selected['item'].fire
        self.ids.health.text = str(self.health)
        self.minus_fire_label = MinusLabel(text=str(-app.selected['item'].fire), center_x=self.center_x,
                                           center_y=self.center_y)
        app.root.get_screen("gamefield").children[0].add_widget(self.minus_fire_label)
        animation = Animation(center_y=(self.center_y + self.size[0]//1.5), d=0.8)
        animation.bind(on_complete=self._kill_label)
        animation.start(self.minus_fire_label)
        app.root.get_screen("gamefield").children[0].my_units[app.selected['num']].canvas.after.get_group('a')[
            0].rgba = (1, 1, 1, 0.0)
        app.selected = None

    def _kill_label(self, *args):
        app = App.get_running_app()
        app.root.get_screen("gamefield").children[0].remove_widget(self.minus_fire_label)


class BattleCardReserve(ButtonBehavior, Image, BoxLayout):

    def __init__(self, **kwargs):
        super(BattleCardReserve, self).__init__(**kwargs)
        Clock.schedule_once(self.finish_init, 0)

    def finish_init(self, td):
        cards = importlib.import_module("ui.units")
        class_ = getattr(cards, self.card)
        a = class_((14, 88), True)
        self.source = a.source

    def selected(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").children[0].my_units[app.selected['num']].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
            app.selected = {}

        if self.parent.children.index(self) != app.card_in_reserve and not app.moving:
            clear_green_blank_cell()
            if app.card_in_reserve is not None:
                self.parent.children[app.card_in_reserve].pos[1] -= 50
            self.pos[1] = self.pos[1] + 50
            app.card_in_reserve = self.parent.children.index(self)

            draw_widget = [x for x in app.root.get_screen("gamefield").ids.gamefield.children if str(type(x)) == "<class 'ui.cards.EmptyField'>" and x.field_pos in ([0,1], [1,1], [1,0])]
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
                   str(type(x)) == "<class 'ui.cards.EmptyField'>" and x.field_pos in ([0, 1], [1, 1], [1, 0])]
    for wid in draw_widget:
        for obj in wid.draw_obj:
            wid.canvas.remove(obj)
        wid.draw_obj = []


class EmptyField(Button):

    def __init__(self, **kwargs):
        #self.field_pos = field_pos

        self.draw_obj = []
        super(EmptyField, self).__init__(**kwargs)

    def move(self):
        app = App.get_running_app()
        if app.selected:
            app.root.get_screen("gamefield").children[0].my_units[app.selected['num']].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
            app.occupied_cells.remove(app.root.get_screen("gamefield").children[0].my_units[app.selected['num']].field_pos)
            app.root.get_screen("gamefield").children[0].my_units[app.selected['num']].field_pos = self.field_pos
            app.occupied_cells.append(self.field_pos)

            animation = Animation(pos=self.pos)
            app.moving = True
            animation.bind(on_complete=self.unblock)
            animation.start(app.selected['item'])
            app.selected = None
            return

        if app.card_in_reserve is not None and self.field_pos in ([0, 1], [1, 1], [1, 0]):
            pos_x = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[0] + app.card_size
            pos_y = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[1]

            cards = importlib.import_module("ui.units")
            class_ = getattr(cards, app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].card)
            unit = class_(source='imgs/stab1.png', pos=(pos_x, pos_y),
                                        size=(app.card_size, app.card_size),
                                        size_hint=(None, None), field_pos=self.field_pos, my_unit=True)
            app.root.get_screen("gamefield").children[0].my_units.append(unit)
            app.root.get_screen("gamefield").children[0].add_widget(unit)
            app.root.get_screen("gamefield").children[0].my_units.append(unit)
            app.occupied_cells.append(self.field_pos)
            animation = Animation(pos=self.pos)
            app.moving = True
            animation.bind(on_complete=self.unblock)
            animation.start(unit)
            app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.remove_widget(app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve])
            app.root.get_screen("gamefield").ids.reserve_cards.data.remove({"card": 'LehrStab'})
            app.root.get_screen("gamefield").ids.reserve_cards.refresh_from_data()
            app.card_in_reserve = None
            clear_green_blank_cell()

    def unblock(self, *args):
        app = App.get_running_app()
        app.moving = False


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


class MinusLabel(Label):
    pass
