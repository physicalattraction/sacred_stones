from monster.monster import Monster


class Goblin(Monster):
    IMAGE = 'goblin.png'
    IMAGE_DEAD = 'goblin_dead.png'
    NAMES = ['Groblin', 'Gobblin', 'Grumlin', 'Skarlin', 'Snaglin', 'Griblin', 'Gibblin', 'Grotlin', 'Grulkin', 'Grell']

    identifier = 'goblin'

    def __init__(self, **kwargs):
        self.hit_points = 10
        self.kind = 'Goblin'
        self.armor = 0
        self.max_damage = 3
        self.chance_to_hit = 80
        self.max_hit_points = 10
        super().__init__(**kwargs)

    def __str__(self):
        return f'{self.kind} {self.name}'


Monster.register(Goblin.identifier, Goblin)
