import random

from monster.monster import Monster


class Goblin(Monster):
    IMAGE = 'goblin.png'
    IMAGE_DEAD = 'goblin_dead.png'
    NAMES = ['Groblin', 'Gobblin', 'Grumlin', 'Skarlin', 'Snaglin', 'Griblin', 'Gibblin', 'Grotlin', 'Grulkin', 'Grell']

    identifier = 'goblin'

    def __init__(self, **kwargs):
        self.kind = 'Goblin'
        self.armor = 0
        self.max_damage = 4
        self.chance_to_hit = 75
        self.max_hit_points = 14
        self.hit_points = 14
        super().__init__(**kwargs)

    @property
    def gold_when_killed(self) -> int:
        return random.choice(range(20, 100))

    @property
    def experience_when_killed(self) -> int:
        return 30

    def __str__(self):
        return f'{self.kind} {self.name}'


Monster.register(Goblin.identifier, Goblin)
