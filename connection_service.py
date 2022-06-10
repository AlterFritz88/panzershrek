import socketio
from kivy.app import App

app = App.get_running_app()
sio = socketio.Client()


def create_connection():
    try:
        sio.connect('http://127.0.0.1:5000')
    except socketio.exceptions.ConnectionError:
        print("Connection error")


def give_me_a_partner():
    sio.emit("give_me_a_partner", {"name": "Adolf"})


@sio.on("init_game")
def status(data):
    app = App.get_running_app()
    app.enemy = {"name": data["enemy_name"], "sid": data["enemy_sid"]}
    print(app.enemy)
    # if data["who_first"] == app.my_name:
    #     app.game_session.my_turn()
    # else:
    #     app.game_session.wait_another_player()
