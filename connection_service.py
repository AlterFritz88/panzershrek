import socketio
from kivy.app import App


sio = socketio.Client()


def create_connection():
    try:
        sio.connect('http://127.0.0.1:5000')
    except socketio.exceptions.ConnectionError:
        print("Connection error")


def give_me_a_partner():
    sio.emit("give_me_a_partner", {"name": "Adolf"})


def my_turn(start_pos, finish_pos, fire):
    app = App.get_running_app()
    sio.emit("turn", {"sid": app.enemy["sid"], "start_pos": start_pos,
                      "finish_pos": finish_pos,
                      "fire": fire})


def my_turn_ends():
    app = App.get_running_app()
    sio.emit("my_turn_ends", {"sid":  app.enemy["sid"]})


def card_from_reserve(start_pos, finish_pos, unit_name, unit_source, unit_type, unit_attack_points,
                      unit_defence_points, fuel_add, price, card_in_reserve):
    app = App.get_running_app()
    sio.emit("card_from_reserve", {"sid": app.enemy["sid"], "start_pos": start_pos,
                                   "finish_pos": finish_pos, "unit_name": unit_name, "unit_source": unit_source,
                                   "unit_type": unit_type, "unit_attack_points": unit_attack_points,
                                   "unit_defence_points": unit_defence_points, "unit_fuel_add": fuel_add,
                                   "unit_price": price, "card_in_reserve": card_in_reserve})


@sio.on("init_game")
def status(data):
    app = App.get_running_app()
    app.enemy = {"name": data["enemy_name"], "sid": data["enemy_sid"], 'first': data['first']}


@sio.on("enemies_turn")
def enemies_turn(data):
    app = App.get_running_app()
    app.enemies_turn = {"unit_pos_start": data["unit_pos_start"],
                        "unit_pos_finish": data["unit_pos_finish"],
                        "fire": data["fire"]}


@sio.on("enemies_card_from_reserve")
def enemies_card_from_reserve(data):
    app = App.get_running_app()
    app.card_from_reserve = {"start_pos": data["start_pos"],
                             "finish_pos": data["finish_pos"], "unit_name": data["unit_name"],
                             "unit_source": data["unit_source"],
                             "unit_type": data["unit_type"], "unit_attack_points": data["unit_attack_points"],
                             "unit_defence_points": data["unit_defence_points"], "card_in_reserve": data["card_in_reserve"]}


@sio.on("enemies_end_turn")
def enemies_card_from_reserve(data):
    app = App.get_running_app()
    app.enemies_end_turn = True


@sio.on("enemies_turn")
def enemies_turn(data):
    app = App.get_running_app()
    app.enemies_turn = True
