import json
import os.path
from typing import List, Dict, TypedDict, Tuple, Set, Literal, Optional

import pygame

from constants import DATA_DIR
from environment import Obstacle, Walkable

OBSTACLE = 'obstacle'
WALKABLE = 'walkable'


class MonsterAssignment(TypedDict):
    name: str
    kind: str


class CellDefinition(TypedDict, total=False):
    # TODO: Investigate why PyCharm is complaining about this type hinting
    tile: Literal[OBSTACLE, WALKABLE]
    player: bool
    monster: MonsterAssignment


ZoneMapRepr = List[str]  # Textual representation of the map
MapLegend = Dict[str, CellDefinition]  # Mapping from each character in the map to its info


class ZoneMap:
    """
    Represents the environment of a zone
    """

    _obstacles: List[Obstacle]
    _walkables: List[Walkable]

    _obstacle_coordinates: Set[Tuple[int, int]]
    _walkable_coordinates: Set[Tuple[int, int]]

    _all_sprites: Optional[pygame.sprite.Group]

    def __init__(self, obstacles: List[Obstacle], walkables: List[Walkable]):
        self._obstacles = obstacles
        self._walkables = walkables

        self._obstacle_coordinates = {(tile.x, tile.y) for tile in obstacles}
        self._walkable_coordinates = {(tile.x, tile.y) for tile in walkables}
        self._validate_obstacles_and_walkables()

        self._all_sprites = None

    @classmethod
    def load(cls, identifier: str):
        obstacles = []
        walkables = []
        world_map, map_legend = cls.read_map(identifier)
        for y, row in enumerate(world_map):
            for x, cell_char in enumerate(row):
                try:
                    cell_info = map_legend[cell_char]
                except KeyError as e:
                    raise KeyError(f'Map character {cell_char} is not defined in map_legend') from e
                tile = cell_info['tile']
                if tile == OBSTACLE:
                    obstacles.append(Obstacle(x=x, y=y))
                elif tile == WALKABLE:
                    walkables.append(Walkable(x=x, y=y))
                else:
                    raise ValueError(f'Tile {tile} is neither obstacle nor walkable')
        return cls(obstacles=obstacles, walkables=walkables)

    @staticmethod
    def read_map(identifier: str) -> Tuple[ZoneMapRepr, MapLegend]:
        """
        Read the map.txt and map_legend.json files for the current zone
        """

        # TODO: Prevent reading the files twice

        print(f'Reading map {identifier}')
        map_legend_file = os.path.join(DATA_DIR, 'original', 'zones', identifier, 'map_legend.json')
        with open(map_legend_file, 'r') as f:
            map_legend = json.load(f)
        map_file = os.path.join(DATA_DIR, 'original', 'zones', identifier, 'map.txt')
        with open(map_file, 'r') as f:
            world_map = [i.strip() for i in f.readlines()]
        return world_map, map_legend

    @property
    def all_sprites(self) -> pygame.sprite.Group():
        if not self._all_sprites:
            self._all_sprites = pygame.sprite.Group(*self._obstacles, *self._walkables)
        return self._all_sprites

    def tile_is_obstacle(self, x: int, y: int) -> bool:
        return (x, y) in self._obstacle_coordinates

    def tile_is_walkable(self, x: int, y: int) -> bool:
        return (x, y) in self._walkable_coordinates

    # Helper methods

    def _validate_obstacles_and_walkables(self):
        assert len(self._obstacle_coordinates) == len(self._obstacles), 'Each obstacle should have unique coordinates'
        assert len(self._walkable_coordinates) == len(self._walkables), 'Each walkable should have unique coordinates'
        assert len(self._obstacle_coordinates.intersection(self._walkable_coordinates)) == 0, \
            'A tile cannot be obstacle and walkable at the same time'
