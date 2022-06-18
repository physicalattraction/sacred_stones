"""
Abstract base classes for anything that can be drawn as a tile on the map
"""

import os
from abc import ABC

import pygame

import constants
from utils import Direction


class Tile(pygame.sprite.Sprite, ABC):
    IMAGE: str = ''  # Must be set by concrete implementations

    x: int  # X-position on the map
    y: int  # Y-position on the map
    image: pygame.Surface  # Image on the map
    rect: pygame.Rect  # Rectangle on the map

    def __init__(self, *, x: int, y: int):
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
        filepath = os.path.join(constants.DATA_DIR, 'images', image_name)
        try:
            return pygame.image.load(filepath).convert_alpha()
        except Exception as e:
            s = f'Couldn\'t open {filepath}: {e}'
            raise ValueError(s) from e


class OrientedTile(Tile, ABC):
    direction: Direction

    def __init__(self, direction: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = constants.DOWN  # This is how the initial image is oriented
        self.orient_towards(direction)  # This is how the tile should be oriented

    def orient_towards(self, direction: Direction):
        angle_to_turn = direction - self.direction
        self.image = pygame.transform.rotate(self.image, angle_to_turn)
        self.direction = direction
