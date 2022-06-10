import os
import ui.cards as cards


class Stab(cards.BattleCard):

    def __init__(self, field_pos, my_unit, attack_points, health_points, price, fuel_add, unit_type, **kwargs):
        self.field_pos = field_pos
        self.my_unit = my_unit

        self.size_hint = (None, None)
        self.fire = 2
        self.health = 20
        self.type = 'stab'
        if self.my_unit:
            self.border_color = (0, 0.8, 0.5, 0.5)
        else:
            self.border_color = (0.8, 0, 0.2, 0.5)
        super(Stab, self).__init__(field_pos, my_unit, attack_points, health_points, price, fuel_add, unit_type, **kwargs)
        self.ids.health_points.text = str(self.health)
        self.ids.attack_points.text = str(self.fire)
        self.source = os.path.join('imgs', 'stab1.png')



