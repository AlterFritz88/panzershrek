import json, random, os
from threading import Thread
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from ui.gamefield import BattleField
from ui.cards import BattleCardReserve, BattleCard, EnemyReserveCard, clear_green_blank_cell
from connection_service import give_me_a_partner, my_turn_ends


class GameSession:
    enemy = 'ai'
    status = 'my_step'


    def __init__(self):
        app = App.get_running_app()
        app.enemy = None
        app.card_from_reserve = None

    def give_me_a_partner(self):
        give_me_a_partner()
        looking_for_a_partner_thred = Thread(target=self.looking_for_a_partner)
        looking_for_a_partner_thred.daemon = True
        looking_for_a_partner_thred.start()

    def looking_for_a_partner(self):
        app = App.get_running_app()
        while True:
            if app.enemy:
                Clock.schedule_once(self.render_field)
                break
            else:
                pass

    def render_field(self, dt):
        app = App.get_running_app()
        self.my_player = Player()
        app.root.get_screen("gamefield").ids.my_player_fuel_add.text = next_step_fuel_adding()
        app.root.current = "gamefield"
        Clock.schedule_once(self.add_stabs)

    def add_stabs(self, td):
        app = App.get_running_app()
        app.card_size = app.root.get_screen("gamefield").ids["0,0"].height
        headquarter_my = BattleCard(field_pos=(0, 0), my_unit=True, attack_points=1, health_points=20, price=0,
                                    fuel_add=4, name="LehrStab",
                                    unit_type="stab",
                                    pos=app.root.get_screen("gamefield").ids['0,0'].pos,
                                    size=(app.card_size, app.card_size), size_hint=(None, None),
                                    source=os.path.join('imgs', 'stab1.png'))
        app.root.get_screen("gamefield").children[0].my_units.append(headquarter_my)
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_my)

        headquarter_enemy = BattleCard(field_pos=(2, 4), my_unit=False, attack_points=1, health_points=20,
                                       price=0, fuel_add=4, unit_type="stab", name="LehrStab",
                                       pos=app.root.get_screen("gamefield").ids['2,4'].pos,
                                       size=(app.card_size, app.card_size),
                                       size_hint=(None, None), source=os.path.join('imgs', 'stab1.png'))
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_enemy)
        self.my_player.load_deck()
        self.give_reserve_card(6)
        render_enemy_new_reserve_card(6)
        app.root.get_screen("gamefield").ids.my_player_fuel.text = str(count_current_fuel())

        if app.enemy['first']:
            block_ui_for_enemy_turn()
            app.enemies_end_turn = False
            app.enemy_turn = True
            app.enemies_turn = False
            wait_enemy_turn_thread = Thread(target=self.wait_another_player)
            wait_enemy_turn_thread.daemon = True
            wait_enemy_turn_thread.start()
        else:
            app.enemy_turn = False

    def give_reserve_card(self, num_cards):
        app = App.get_running_app()
        random.shuffle(self.my_player.deck)
        random_init_reserv_cards = [self.my_player.deck.pop(x) for x in num_cards * [0]]

        for unit in random_init_reserv_cards:
            app.root.get_screen("gamefield").ids.reserve_cards.children[0].add_widget(
                BattleCardReserve(attack_points=unit.attack_points, health_points=unit.health_points,
                                  source=os.path.join('imgs', unit.img), price=unit.price, fuel_add=unit.fuel_add,
                                  unit_type=unit.unit_type, size=(app.card_size//1.5, app.card_size//1.5)))

    def next_turn(self):
        app = App.get_running_app()
        app.card_in_reserve = None
        app.root.get_screen("gamefield").ids.my_player_fuel.text = str(
            int(app.root.get_screen("gamefield").ids.my_player_fuel.text) + int(next_step_fuel_adding()))
        self.give_reserve_card(1)
        # units_to_be_free = [x for x in app.root.get_screen("gamefield").children[0].children if
        #                     str(type(x)) == "<class 'ui.cards.BattleCard'>"]
        # for unit in units_to_be_free:
        #     unit.enable()
        block_ui_for_enemy_turn()
        my_turn_ends()
        if app.selected:
            app.selected['item'].canvas.after.get_group('a')[0].rgba = (1, 1, 1, 0.0)
            app.selected = None
        app.enemy_turn = True
        app.enemies_end_turn = False
        app.enemies_turn = False
        clear_green_blank_cell()
        wait_enemy_turn_thread = Thread(target=self.wait_another_player)
        wait_enemy_turn_thread.daemon = True
        wait_enemy_turn_thread.start()

    def wait_another_player(self):
        app = App.get_running_app()
        while app.enemy_turn:
            if app.card_from_reserve:
                render_enemies_reserve_spawn()
            if app.enemies_end_turn:
                unblock_my_units()
                render_enemy_new_reserve_card(1)
                app.enemy_turn = False
            if app.enemies_turn:
                render_enemies_turn()
                app.enemies_turn = None


def count_current_fuel(my_army=True):
    app = App.get_running_app()
    temp_fuel = int(app.root.get_screen("gamefield").ids.my_player_fuel.text)
    for unit in app.root.get_screen("gamefield").children[0].children:
        if unit.__class__.__name__ == "BattleCard" and unit.my_unit == my_army:
            temp_fuel += unit.fuel_add
    return temp_fuel


def next_step_fuel_adding(my_army=True):
    app = App.get_running_app()
    temp_fuel = 0
    for unit in app.root.get_screen("gamefield").children[0].children:
        if unit.__class__.__name__ == "BattleCard" and unit.my_unit == my_army:
            temp_fuel += unit.fuel_add

    if temp_fuel >= 0:
        temp_fuel = "+" + str(temp_fuel)
    else:
        temp_fuel = str(temp_fuel)

    return temp_fuel


def render_enemy_new_reserve_card(num_cards):
    app = App.get_running_app()
    enemy_reserve_cards = [EnemyReserveCard(size=(app.card_size // 1.5, app.card_size // 1.5)) for x in range(num_cards)]
    for enemy_reserve_card in enemy_reserve_cards:
        app.root.get_screen("gamefield").ids.enemy_reserve_cards.children[0].add_widget(enemy_reserve_card)


class Player:
    deck = []

    def load_deck(self):
        with open('work_files/player1_units.json', 'r') as f:
            player_server_deck = json.load(f)
            self.deck = [PlayerUnit(x["name"], x["img"], x['attack_points'], x['health_points'],
                                    x["price"], x["fuel_add"], x['unit_type']) for x in player_server_deck]


class PlayerUnit:

    def __init__(self, name, img, attack_points, health_points, price, fuel_add, unit_type):
        self.name = name
        self.img = img
        self.attack_points = attack_points
        self.health_points = health_points
        self.price = price
        self.fuel_add = fuel_add
        self.unit_type = unit_type


def block_ui_for_enemy_turn():
    app = App.get_running_app()
    units_to_be_blocked = [x for x in app.root.get_screen("gamefield").children[0].children if
                        str(type(x)) == "<class 'ui.cards.BattleCard'>" and x.my_unit]
    for unit in units_to_be_blocked:
        unit.disable()


def unblock_my_units():
    app = App.get_running_app()
    units_to_be_unblocked = [x for x in app.root.get_screen("gamefield").children[0].children if
                           str(type(x)) == "<class 'ui.cards.BattleCard'>" and x.my_unit]
    for unit in units_to_be_unblocked:
        unit.enable()


def render_enemies_reserve_spawn():
    app = App.get_running_app()
    unit_relative_pos = app.root.get_screen("gamefield").ids.enemy_reserve_cards.children[0].children[
        app.card_from_reserve["card_in_reserve"]].pos
    start_pos = [unit_relative_pos[0], app.root.get_screen("gamefield").ids.enemy_reserve_cards.pos[1]]

    new_enemy_unit = BattleCard(field_pos=app.card_from_reserve["finish_pos"], my_unit=False,
                                name=app.card_from_reserve["unit_name"],
                                attack_points=app.card_from_reserve["unit_defence_points"],
                                health_points=app.card_from_reserve["unit_defence_points"],
                                fuel_add=app.card_from_reserve["unit_name"],
                                unit_type=app.card_from_reserve["unit_type"], price=app.card_from_reserve["unit_name"],
                                size_hint=(None, None),
                                size=(app.card_size, app.card_size), source=app.card_from_reserve["unit_source"],
                                pos=start_pos)
    app.root.get_screen("gamefield").children[0].add_widget(new_enemy_unit)

    animation = Animation(pos=app.root.get_screen("gamefield").ids[",".join(str(x) for x in new_enemy_unit.field_pos)].pos, duration=0.3)
    animation.start(new_enemy_unit)
    app.root.get_screen("gamefield").ids.enemy_reserve_cards.children[0].remove_widget(
        app.root.get_screen("gamefield").ids.enemy_reserve_cards.children[0].children[
            app.card_from_reserve["card_in_reserve"]])
    app.card_from_reserve = None


def render_enemies_turn():
    app = App.get_running_app()
    for x in app.root.get_screen("gamefield").children[0].children:
        if str(type(x)) == "<class 'ui.cards.BattleCard'>" and not x.my_unit and tuple(x.field_pos) == tuple(
                app.enemies_turn["start_pos"]):
            who_moving = x

    if not app.enemies_turn["fire"]:
        end_point = [x for x in app.root.get_screen("gamefield").ids.gamefield.children if
                     tuple(x.field_pos) == tuple(app.enemies_turn["finish_pos"])][0]
        animation = Animation(pos=end_point.pos, duration=0.3)
        animation.start(who_moving)
        who_moving.field_pos = tuple(app.enemies_turn["finish_pos"])

    else:
        for x in app.root.get_screen("gamefield").children[0].children:
            if str(type(x)) == "<class 'ui.cards.BattleCard'>" and x.my_unit and tuple(x.field_pos) == tuple(
                    app.enemies_turn["finish_pos"]):
                end_point = x
        end_point.attack(who_moving)



