import json, random, os
from threading import Thread
from kivy.app import App
from kivy.clock import Clock
from ui.gamefield import BattleField
from ui.cards import BattleCardReserve, BattleCard, EnemyReserveCard
from connection_service import give_me_a_partner


class GameSession:
    enemy = 'ai'
    status = 'my_step'

    def __init__(self):
        app = App.get_running_app()
        app.enemy = None

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
                                    fuel_add=4,
                                    unit_type="stab",
                                    pos=app.root.get_screen("gamefield").ids['0,0'].pos,
                                    size=(app.card_size, app.card_size), size_hint=(None, None),
                                    source=os.path.join('imgs', 'stab1.png'))
        app.root.get_screen("gamefield").children[0].my_units.append(headquarter_my)
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_my)

        headquarter_enemy = BattleCard(field_pos=(2, 4), my_unit=False, attack_points=1, health_points=20,
                                       price=0, fuel_add=4, unit_type="stab",
                                       pos=app.root.get_screen("gamefield").ids['2,4'].pos,
                                       size=(app.card_size, app.card_size),
                                       size_hint=(None, None), source=os.path.join('imgs', 'stab1.png'))
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_enemy)
        app.occupied_cells.append((2, 4))
        app.occupied_cells.append((0, 0))
        self.my_player.load_deck()
        self.give_reserve_card(6)
        enemy_reserve_cards = [EnemyReserveCard(size=(app.card_size//1.5, app.card_size//1.5)) for x in range(6)]
        for enemy_reserve_card in enemy_reserve_cards:
            app.root.get_screen("gamefield").ids.enemy_reserve_cards.children[0].add_widget(enemy_reserve_card)
        app.root.get_screen("gamefield").ids.my_player_fuel.text = str(count_current_fuel())


    def give_reserve_card(self, num_cards):
        app = App.get_running_app()
        random.shuffle(self.my_player.deck)
        random_init_reserv_cards = [self.my_player.deck.pop(x) for x in num_cards * [0]]  # удаляю 6 элементов из деки

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
        units_to_be_free = [x for x in app.root.get_screen("gamefield").children[0].children if
                            str(type(x)) == "<class 'ui.cards.BattleCard'>"]
        for unit in units_to_be_free:
            unit.enable()

    def wait_another_player(self):
        pass


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
