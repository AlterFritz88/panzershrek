import json, random, os
from kivy.app import App
from ui.gamefield import BattleField, Stab
from ui.cards import BattleCardReserve


class GameSession:
    enemy = 'ai'
    status = 'my_step'

    def __init__(self):
        app = App.get_running_app()
        self.my_player = Player()
        self.my_player.load_deck()
        app.card_size = app.root.get_screen("gamefield").ids.gamefield.height // 2.1
        app.root.get_screen("gamefield").add_widget(BattleField())
        headquarter_my = Stab(field_pos=(0, 0), my_unit=True, attack_points=1, health_points=20,
                              pos=app.root.get_screen("gamefield").ids['0,0'].pos,
                              size=(app.card_size, app.card_size), size_hint=(None, None))
        app.root.get_screen("gamefield").children[0].my_units.append(headquarter_my)
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_my)

        headquarter_enemy = Stab(field_pos=(1, 4), my_unit=False, attack_points=1, health_points=20,
                                 pos=app.root.get_screen("gamefield").ids['2,4'].pos,
                                 size=(app.card_size, app.card_size),
                                 size_hint=(None, None))
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_enemy)

        app.occupied_cells.append((2, 4))
        app.occupied_cells.append((0, 0))
        self.give_reserve_card()
        self.my_player.current_fuel = 4
        print(app.root.get_screen("gamefield").ids)
        app.root.get_screen("gamefield").ids.my_player_fuel.text = str(self.my_player.current_fuel)

    def give_reserve_card(self):
        app = App.get_running_app()
        random.shuffle(self.my_player.deck)
        random_init_reserv_cards = [self.my_player.deck.pop(x) for x in 6 * [0]]  # удаляю 6 элементов из деки

        for unit in random_init_reserv_cards:
            app.root.get_screen("gamefield").ids.reserve_cards.children[0].add_widget(
                BattleCardReserve(attack_points=unit.attack_points, health_points=unit.health_points,
                                  source=os.path.join('imgs', unit.img)))

    def players_step(self):
        pass

    def wait_another_player(self):
        pass


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
