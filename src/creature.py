from abc import ABC
from typing import TypedDict

from saveable import Saveable
from tile import Tile


class CreatureDict(TypedDict):
    """
    JSON representation of a creature's state
    """

    name: str
    kind: str
    x: int
    y: int
    armor: int
    max_damage: int
    chance_to_hit: int
    max_hit_points: int
    hit_points: int


class Creature(Tile, Saveable, ABC):
    # TODO: Should Creature have its own load() and save() method? If not, why not?

    IMAGE_DEAD: str = None

    name: str
    kind: str
    armor: int
    max_damage: int
    chance_to_hit: int
    max_hit_points: int
    hit_points: int

    def __init__(self, *, hit_points: int = None, **kwargs):
        self.hit_points = hit_points if hit_points is not None else self.max_hit_points
        super().__init__(**kwargs)

    def calculate_damage(self, enemy: 'Creature') -> int:
        # TODO: More sophisticated way to calculate damage
        return self.max_damage - enemy.armor

    def is_dead(self):
        return self.hit_points <= 0

    @property
    def image_name(self) -> str:
        if self.is_dead():
            return self.IMAGE_DEAD or self.IMAGE  # Fallback to IMAGE if there is no IMAGE_DEAD
        else:
            return self.IMAGE
