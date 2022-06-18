import json
import os.path
from typing import List, TypedDict, Optional

import pygame

from constants import DATA_DIR
from environment import Walkable, Obstacle
from monster.monster import MonsterDict, Monster
from saveable import Saveable
from zonemap import ZoneMap


class ZoneDict(TypedDict):
    """
    JSON representation of a zone's state
    """

    identifier: str
    monsters: List[MonsterDict]


class Zone(Saveable):
    identifier: str
    walkables: List[Walkable]
    obstacles: List[Obstacle]
    monsters: List[Monster]

    _all_sprites: Optional[pygame.sprite.Group]

    def __init__(self, identifier: str, monsters: List[Monster]):
        self.map = ZoneMap.load(identifier)
        self.identifier = identifier
        self.monsters = monsters

        self._all_sprites = None

    # Saveable methods

    @classmethod
    def get_filepath(cls, identifier: str):
        zones_dir = os.path.join(DATA_DIR, 'current', 'zones')
        if not os.path.isdir(zones_dir):
            os.mkdir(zones_dir)
        # TODO: Remove hardcoded `current` when implementing save slots
        return os.path.join(zones_dir, f'{identifier}.json')

    @classmethod
    def from_json(cls, data: ZoneDict) -> 'Zone':
        """
        Return a Zone object from the given zone state information
        """

        identifier = data['identifier']
        monsters = [Monster.from_json(monster) for monster in data['monsters']]
        return cls(identifier=identifier, monsters=monsters)

    @classmethod
    def load(cls, identifier: str) -> 'Zone':
        """
        Load the zone from /data/current/zones/<identifier>.json

        :param identifier: Zone identifier to load
        """

        filepath = cls.get_filepath(identifier)
        if not os.path.isfile(filepath):
            # The zone has not been visited yet
            return cls._init_zone_from_map(identifier)
        else:
            return cls._init_zone_from_state(filepath)

    def as_json(self) -> ZoneDict:
        """
        Return the zone state information
        """

        return {'identifier': self.identifier,
                'monsters': [monster.as_json() for monster in self.monsters]}

    def save(self):
        """
        Save the zone state information to /data/current/zones/<identifier>.json
        """

        with open(self.get_filepath(self.identifier), 'w') as f:
            json.dump(self.as_json(), f, indent=2)

    # Methods for clients

    @property
    def all_sprites(self) -> pygame.sprite.Group():
        if not self._all_sprites:
            self._all_sprites = pygame.sprite.Group(*self.map.all_sprites, *self.monsters)
        return self._all_sprites

    def monster_on_tile(self, x: int, y: int) -> Optional[Monster]:
        """
        Return the _monster on the given tile, or None if there is no _monster on the tile
        """

        return next((monster for monster in self.monsters if monster.x == x and monster.y == y), None)

    # Helper methods

    @classmethod
    def _init_zone_from_state(cls, filepath: str) -> 'Zone':
        with open(filepath, 'r') as f:
            data = json.load(f)
            return cls.from_json(data)

    @classmethod
    def _init_zone_from_map(cls, identifier: str) -> 'Zone':
        monsters = []
        world_map, map_legend = ZoneMap.read_map(identifier)
        for y, row in enumerate(world_map):
            for x, cell_char in enumerate(row):
                try:
                    cell_info = map_legend[cell_char]
                except KeyError as e:
                    raise KeyError(f'Map character {cell_char} is not defined in map_legend') from e
                if monster_info := cell_info.get('monster'):
                    monsters.append(Monster.from_json(monster_info, x=x, y=y))
        return cls(identifier=identifier, monsters=monsters)
