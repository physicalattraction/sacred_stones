import json
import os
from abc import ABC
from typing import List, Dict

import pygame

import constants
from utils import Direction, convert_direction_to_dx_dy, DATA_DIR


class Tile(pygame.sprite.Sprite, ABC):
    IMAGE: str = ''

    x: int  # X-position on the map
    y: int  # Y-position on the map
    image: pygame.Surface  # Image on the map
    rect: pygame.Rect  # Rectangle on the map

    def __init__(self, x: int, y: int):
        assert self.IMAGE, f'Tile {self.__class__.__name__} has no map image defined'
        super().__init__()
        self.x = x
        self.y = y
        self.image = self._load_image(self.image_name)
        self.place_on_screen(constants.TILESIZE, x, y)

    @property
    def image_name(self) -> str:
        return self.IMAGE

    def place_on_screen(self, tilesize: int, x: int, y: int):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * tilesize, y * tilesize)

    def _load_image(self, image_name: str) -> pygame.Surface:
        filepath = os.path.join(DATA_DIR, 'images', image_name)
        try:
            return pygame.image.load(filepath).convert_alpha()
        except Exception as e:
            s = f'Couldn\'t open {filepath}: {e}'
            raise ValueError(s) from e


class Obstacle(Tile):
    IMAGE = constants.WALL_IMG


class Walkable(Tile):
    IMAGE = constants.GRASS_IMG


class Creature(Tile, ABC):
    IMAGE_DEAD: str
    DATA_FILE: str

    name: str
    kind: str
    armor: int
    max_damage: int
    chance_to_hit: int
    max_hit_points: int
    hit_points: int

    def __init__(self, name: str, kind: str, armor: int, max_damage: int,
                 chance_to_hit: int, max_hit_points: int, hit_points: int,
                 *args, **kwargs):
        self.name = name
        self.kind = kind
        self.armor = armor
        self.max_damage = max_damage
        self.chance_to_hit = chance_to_hit
        self.max_hit_points = max_hit_points
        self.hit_points = hit_points
        super().__init__(*args, **kwargs)

    def calculate_damage(self, enemy: 'Creature') -> int:
        # TODO: More sophisticated way to calculate damage
        return self.max_damage - enemy.armor

    def is_dead(self):
        return self.hit_points <= 0

    def as_json(self) -> Dict:
        return {
            field: getattr(self, field)
            for field in ('name', 'kind', 'x', 'y', 'armor', 'max_damage', 'chance_to_hit',
                          'max_hit_points', 'hit_points')
        }

    @classmethod
    def from_json(cls, data: Dict) -> 'Creature':
        return cls(**data)

    def save(self):
        filepath = os.path.join(DATA_DIR, self.DATA_FILE)
        with open(filepath, 'w') as f:
            json.dump(self.as_json(), f, indent=2)

    @classmethod
    def load(cls) -> 'Creature':
        filepath = os.path.join(DATA_DIR, cls.DATA_FILE)
        with open(filepath, 'r') as f:
            return cls.from_json(json.load(f))

    @property
    def image_name(self) -> str:
        if self.is_dead():
            return self.IMAGE_DEAD or self.IMAGE
        else:
            return self.IMAGE


class OrientedTile(Tile, ABC):
    direction: Direction

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = constants.DOWN

    def orient_towards(self, direction: Direction):
        angle_to_turn = direction - self.direction
        self.image = pygame.transform.rotate(self.image, angle_to_turn)
        self.direction = direction


class Player(OrientedTile, Creature):
    IMAGE = constants.PLAYER_IMG
    IMAGE_DEAD = constants.PLAYER_IMG_DEAD
    DATA_FILE = constants.PLAYER_DATA_FILE  # TODO: Remove this dependency

    def move(self, direction: Direction, obstacles: List[Obstacle]):
        # First rotate the image, then move the iamge
        self.orient_towards(direction)
        dx, dy = convert_direction_to_dx_dy(direction)
        if not self._collide_with_obstacles(dx, dy, obstacles):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)

    def _collide_with_obstacles(self, dx: int, dy: int, obstacles: List[Obstacle]) -> bool:
        return any(obstacle.x == self.x + dx and obstacle.y == self.y + dy for obstacle in obstacles)


class Monster(Creature):
    IMAGE = constants.MONSTER_IMG
    IMAGE_DEAD = constants.MONSTER_IMG_DEAD
    DATA_FILE = constants.MONSTER_DATA_FILE
