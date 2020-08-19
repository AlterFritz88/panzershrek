from .cards import BattleCard


class LehrStab(BattleCard):

    def __init__(self, field_pos, my_unit, **kwargs):
        self.field_pos = field_pos
        self.my_unit = my_unit
        self.source = 'imgs/stab1.png'
        self.size_hint = (None, None)
        self.fire = 2
        self.health = 20
        self.type = 'stab'
        if self.my_unit:
            self.border_color = (0, 0.8, 0.5, 0.5)
        else:
            self.border_color = (0.8, 0, 0.2, 0.5)
        super(LehrStab, self).__init__(field_pos, my_unit, **kwargs)
        self.ids.health.text = str(self.health)
        self.ids.fire.text = str(self.fire)
