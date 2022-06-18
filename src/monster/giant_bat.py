from monster.monster import Monster


class GiantBat(Monster):
    IMAGE = 'giant_bat.png'
    IMAGE_DEAD = 'giant_bat_dead.png'
    NAMES = ['Nether', 'Countie']

    identifier = 'giant_bat'

    def __init__(self, **kwargs):
        self.hit_points = 10
        self.kind = 'Giant Bat'
        self.armor = 0
        self.max_damage = 3
        self.chance_to_hit = 80
        self.max_hit_points = 10
        super().__init__(**kwargs)

    def __str__(self):
        return f'{self.kind} {self.name}'


Monster.register(GiantBat.identifier, GiantBat)
