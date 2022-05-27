from kivy.app import App
from ui.gamefield import BattleField, LehrStab


class GameSession:
    enemy = 'ai'
    status = 'my_step'

    def __init__(self):

        app = App.get_running_app()
        app.card_size = app.root.get_screen("gamefield").ids.gamefield.height // 2.1
        app.root.get_screen("gamefield").add_widget(BattleField())
        headquarter_my = LehrStab(field_pos=(0, 0), my_unit=True,
                                  pos=app.root.get_screen("gamefield").ids['0,0'].pos,
                                  size=(app.card_size, app.card_size), size_hint=(None, None))
        app.root.get_screen("gamefield").children[0].my_units.append(headquarter_my)
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_my)

        headquarter_enemy = LehrStab(field_pos=(1, 4), my_unit=False,
                                     pos=app.root.get_screen("gamefield").ids['2,4'].pos,
                                     size=(app.card_size, app.card_size),
                                     size_hint=(None, None))
        app.root.get_screen("gamefield").children[0].add_widget(headquarter_enemy)

        app.occupied_cells.append((2, 4))
        app.occupied_cells.append((0, 0))

    def players_step(self):
        pass

    def wait_another_player(self):
        pass

