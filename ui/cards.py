import time
from itertools import product, starmap
import os
import importlib
import math

from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Color, Line, Rectangle, Rotate, PopMatrix, PushMatrix
from kivy.clock import Clock
from ui import game_session as gs
from connection_service import card_from_reserve, my_turn


class BattleCard(ButtonBehavior, AsyncImage, BoxLayout):
    BANG_RESULT = Image(source=os.path.join('imgs', 'bang.gif'), size_hint=(None, None),
                      anim_delay=-1, anim_loop=1)

    def __init__(self, field_pos, my_unit, attack_points, health_points, price, fuel_add, unit_type, name, **kwargs):
        self.allowed_position_for_move = None
        self.field_pos = field_pos
        self.my_unit = my_unit
        self.attack_points = attack_points
        self.health_points = health_points
        self.unit_type = unit_type
        self.fuel_add = fuel_add
        self.can_move = True
        if self.my_unit:
            self.border_color = (0, 0.8, 0.5, 0.25)
        else:
            self.border_color = (0.8, 0, 0.2, 0.25)
        self.choose_color = (1, 1, 1, 0.0)
        super(BattleCard, self).__init__(**kwargs)
        Clock.schedule_once(self.finish_init, 0)

    def finish_init(self, td):
        self.ids.attack_points.text = str(self.attack_points)
        self.ids.health_points.text = str(self.health_points)
        self.source = self.source

    def select(self):
        app = App.get_running_app()
        if app.card_in_reserve is not None and not self.my_unit:
            app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[1] -= app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].size[0]//5
            app.card_in_reserve = None

        if not self.my_unit and not app.moving and app.selected:
            try:
                app.root.get_screen("gamefield").children[0].remove_widget(self.BANG)
            except AttributeError:
                pass
            #clear_green_blank_cell()
            if app.selected['item'].unit_type in ('stab', 'art'):
                self.attack(app.selected['item'])
            else:
                cells = list(starmap(lambda a, b: (app.selected["item"].field_pos[0] + a, app.selected["item"].field_pos[1] + b),
                                     product((0, -1, +1), (0, -1, +1))))
                if tuple(self.field_pos) in cells:
                    self.attack(app.selected['item'])

        if self.my_unit and not app.moving:
            clear_green_blank_cell()
            if not app.selected:

                app.root.get_screen("gamefield").children[0].remove_widget(self)
                app.root.get_screen("gamefield").children[0].add_widget(self)
                self.canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.95)
                app.selected = {'item': self,
                                'num': app.root.get_screen("gamefield").children[0].children.index(self)}

                if self.can_move:
                    if self.unit_type in ('heavy_tank', 'AT', 'art'):
                        self.allowed_position_for_move = ([self.field_pos[0] + 1, self.field_pos[1]],
                                                           [self.field_pos[0] - 1, self.field_pos[1]],
                                                           [self.field_pos[0], self.field_pos[1] + 1],
                                                           [self.field_pos[0], self.field_pos[1] - 1])
                    elif self.unit_type == "middle_tank":
                        self.allowed_position_for_move = ([self.field_pos[0] + 1, self.field_pos[1]],
                                                          [self.field_pos[0] - 1, self.field_pos[1]],
                                                          [self.field_pos[0], self.field_pos[1] + 1],
                                                          [self.field_pos[0], self.field_pos[1] - 1])
                    elif self.unit_type == "light_tank":
                        self.allowed_position_for_move = list(
                            starmap(lambda a, b: [self.field_pos[0] + a, self.field_pos[1] + b],
                                    product((0, -1, +1), (0, -1, +1))))
                    elif self.unit_type == "armored_car":
                        self.allowed_position_for_move = list(starmap(lambda a, b: [self.field_pos[0] + a, self.field_pos[1] + b],
                                         product((0, -2, +2, -1, +1), (0, -2, +2, -1, +1))))

                    elif self.unit_type == "stab":
                        self.allowed_position_for_move = []

                    draw_widget = [x for x in app.root.get_screen("gamefield").ids.gamefield.children if
                                   str(type(x)) == "<class 'ui.cards.EmptyField'>" and x.field_pos in
                                   self.allowed_position_for_move]
                    paint_fields_in_green(draw_widget)
            else:
                app.root.get_screen("gamefield").children[0].remove_widget(self)
                app.root.get_screen("gamefield").children[0].add_widget(self)

                if app.selected["item"] == self:
                    self.canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
                    app.selected = None
                else:
                    app.selected["item"].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
                    app.selected = None
                    self.select()

    def attack(self, who_attack):
        app = App.get_running_app()
        myradians = math.atan2(self.pos[1] - who_attack.pos[1], self.pos[0] - who_attack.pos[0])
        angle = math.degrees(myradians)
        self.BANG = Bang(source=os.path.join('imgs', 'bullet.png'), pos=who_attack.pos,
                         size=(self.size[0] // 2, self.size[1] // 2),
                         size_hint=(None, None), angle=angle, center_x=who_attack.center_x,
                         center_y=who_attack.center_y)

        app.root.get_screen("gamefield").children[0].add_widget(self.BANG)
        animation = Animation(pos=(self.pos[0] + self.size[1] // 4, self.pos[1] + self.size[1] // 4), d=0.2)
        animation.bind(on_complete=lambda *x: self._kill_bullet(who_attack))
        animation.start(self.BANG)
        my_turn(who_attack.field_pos, self.field_pos, True)

    def _kill_bullet(self, who_attack):
        app = App.get_running_app()
        animation = Animation(pos=(self.pos[0] + 10, self.pos[1]), d=0.05)
        animation += Animation(pos=(self.pos[0] - 10, self.pos[1]), d=0.05)
        animation += Animation(pos=(self.pos[0], self.pos[1]), d=0.1)
        animation.start(self)
        app.root.get_screen("gamefield").children[0].remove_widget(self.BANG)
        app.root.get_screen("gamefield").children[0].remove_widget(self.BANG_RESULT)
        self.BANG_RESULT.pos = self.pos
        self.BANG_RESULT.size = self.size
        self.BANG_RESULT.anim_delay = 0
        app.root.get_screen("gamefield").children[0].add_widget(self.BANG_RESULT)
        self.BANG_RESULT._coreimage.anim_reset(True)
        self.health_points -= who_attack.attack_points
        if self.health_points <= 0:
            animation1 = Animation(opacity=0.05)
            animation1.bind(on_complete=self.kill_unit)
            animation1.start(self)
        self.ids.health_points.text = str(self.health_points)
        self.minus_fire_label = MinusLabel(text=str(-who_attack.attack_points), center_x=self.center_x,
                                           center_y=self.center_y)
        app.root.get_screen("gamefield").children[0].add_widget(self.minus_fire_label)
        animation = Animation(center_y=(self.center_y + self.size[0] // 1.5), d=0.8)
        animation.bind(on_complete=self._kill_label)
        animation.start(self.minus_fire_label)

        if app.selected:
            app.selected['item'].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
            app.selected['item'].disable()
            clear_green_blank_cell()
            app.selected = None

    def _kill_label(self, *args):
        app = App.get_running_app()
        app.root.get_screen("gamefield").children[0].remove_widget(self.minus_fire_label)

    def disable(self):
        self.opacity = 0.6
        self.disabled = True

    def enable(self):
        self.opacity = 1
        self.disabled = False
        self.can_move = True

    def kill_unit(self, *args):
        app = App.get_running_app()
        app.root.get_screen("gamefield").children[0].remove_widget(self)



class BattleCardReserve(ButtonBehavior, AsyncImage, BoxLayout):

    def __init__(self, attack_points, health_points, price, fuel_add, unit_type, **kwargs):
        super(BattleCardReserve, self).__init__(**kwargs)
        Clock.schedule_once(self.finish_init, 0)
        self.health_points = health_points
        self.attack_points = attack_points
        self.price = price
        self.unit_type = unit_type
        self.fuel_add = fuel_add

    def finish_init(self, td):
        self.ids.attack_points.text = str(self.attack_points)
        self.ids.health_points.text = str(self.health_points)
        self.source = self.source

    def selected(self):
        app = App.get_running_app()
        if app.moving:
            return
        if app.selected:
            app.selected['item'].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
            app.selected = None

        if self.parent.children.index(self) != app.card_in_reserve and not app.moving:
            clear_green_blank_cell()
            if app.card_in_reserve is not None:
                self.parent.children[app.card_in_reserve].pos[1] -= self.size[0]//5
            self.pos[1] = self.pos[1] + self.size[0]//5
            app.card_in_reserve = self.parent.children.index(self)

            draw_widget = [x for x in app.root.get_screen("gamefield").ids.gamefield.children if
                           str(type(x)) == "<class 'ui.cards.EmptyField'>" and x.field_pos in ([0, 1], [1, 1], [1, 0])]
            paint_fields_in_green(draw_widget)
        else:
            if app.card_in_reserve is not None:
                clear_green_blank_cell()
                self.pos[1] = self.pos[1] - self.size[0]//5
                app.card_in_reserve = None


def clear_green_blank_cell():
    app = App.get_running_app()
    draw_widget = [x for x in app.root.get_screen("gamefield").ids.gamefield.children if
                   str(type(x)) == "<class 'ui.cards.EmptyField'>"]
    for wid in draw_widget:
        for obj in wid.draw_obj:
            wid.canvas.remove(obj)
        wid.draw_obj = []


class EmptyField(Button):

    def __init__(self, **kwargs):
        # self.field_pos = field_pos
        super(EmptyField, self).__init__(**kwargs)
        self.draw_obj = []

    def move(self):
        app = App.get_running_app()
        if app.selected:
            if self.field_pos in app.selected['item'].allowed_position_for_move:
                app.selected['item'].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
                animation = Animation(pos=self.pos, duration=0.3)
                app.moving = True
                animation.bind(on_complete=lambda *x: unblock(app.selected['item']))
                animation.start(app.selected['item'])
                app.selected['item'].can_move = False
                my_turn(app.selected['item'].field_pos, self.field_pos, False)
                app.selected['item'].field_pos = self.field_pos
                return

        if app.card_in_reserve is not None and self.field_pos in ([0, 1], [1, 1], [1, 0]) and not app.enemy_turn:
            unit = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve]
            parent = app.root.get_screen("gamefield").ids.reserve_cards.to_parent(*unit.pos)
            pos_x = parent[0]
            if unit.price > int(app.root.get_screen("gamefield").ids.my_player_fuel.text):
                animation = Animation(pos=(unit.pos[0] + 5, unit.pos[1]), duration=0.05)
                animation += Animation(pos=(unit.pos[0] - 10, unit.pos[1]), duration=0.05)
                animation += Animation(pos=(unit.pos[0], unit.pos[1]), duration=0.05)
                animation.start(unit)
                return

            pos_y = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve].pos[1]

            unit1 = app.root.get_screen("gamefield").ids.reserve_cards.ids.rs.children[app.card_in_reserve]
            unit = BattleCard(field_pos=self.field_pos, my_unit=True, name=unit1.name,
                              attack_points=unit1.attack_points, health_points=unit1.health_points,
                              fuel_add=unit1.fuel_add, unit_type=unit1.unit_type, price=unit1.price,
                              size_hint=(None, None),
                              size=(app.card_size, app.card_size), source=unit1.source, pos=(pos_x, pos_y))

            app.root.get_screen("gamefield").children[0].add_widget(unit)
            animation = Animation(pos=self.pos, duration=0.3)
            app.moving = True
            animation.bind(on_complete=lambda *x: unblock(unit))
            animation.start(unit)
            app.root.get_screen("gamefield").ids.reserve_cards.children[0].remove_widget(unit1)
            app.root.get_screen("gamefield").ids.my_player_fuel.text = str(int(app.root.get_screen("gamefield").ids.my_player_fuel.text) - unit1.price)
            app.root.get_screen("gamefield").ids.my_player_fuel_add.text = gs.next_step_fuel_adding()

            card_from_reserve(app.card_in_reserve, tuple(self.field_pos), unit1.name, unit1.source, unit1.unit_type,
                              unit1.attack_points,
                              unit1.health_points, unit1.fuel_add, unit1.price, app.card_in_reserve)
            clear_green_blank_cell()


class Bang(AsyncImage):
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


def paint_fields_in_green(fields_widgets):
    for wid in fields_widgets:
        color = Color(0.1, 0.7, 0.3, 0.15)
        rect = Rectangle(pos=wid.pos, size=(wid.width, wid.width))
        wid.canvas.add(color)
        wid.canvas.add(rect)
        wid.draw_obj = [color, rect]


def unblock(unit):
    app = App.get_running_app()
    if app.card_in_reserve:
        if unit.unit_type in ("art", 'heavy_tank', 'middle_tank', 'AT', 'light_tank'):
            unit.disable()
        app.card_in_reserve = None
    unit.allowed_position_for_move = []
    app.moving = False
    app.selected = None
    clear_green_blank_cell()


class EnemyReserveCard(Image):
    app = App.get_running_app()
    source = os.path.join('imgs', 'skirt.png')
    size_hint = (None, None)
    #size = (app.card_size, app.card_size)
