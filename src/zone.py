import json
import os.path
from typing import List, TypedDict, Tuple, Optional

import constants
from constants import DATA_DIR
from environment import Walkable, Obstacle
from map import read_map
from monster import MonsterDict, Monster, monster_definitions
from saveable import Saveable


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

    def __init__(self, identifier: str, monsters: List[Monster]):
        self.obstacles, self.walkables = self._load_environment_from_map(identifier)
        self.identifier = identifier
        self.monsters = monsters

    # Saveable methods

    @classmethod
    def get_filepath(cls, identifier: str):
        # TODO: Remove hardcoded `current` when implementing save slots
        return os.path.join(DATA_DIR, 'current', 'zones', f'{identifier}.json')

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

    def monster_on_tile(self, x: int, y: int) -> Optional[Monster]:
        """
        Return the monster on the given tile, or None if there is no monster on the tile
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
        world_map, map_legend = read_map(identifier)
        for y, row in enumerate(world_map):
            for x, cell_char in enumerate(row):
                try:
                    cell_info = map_legend[cell_char]
                except KeyError as e:
                    raise KeyError(f'Map character {cell_char} is not defined in map_legend') from e
                if monster_info := cell_info.get('monster'):
                    kind = monster_info['kind']
                    monster_definition = monster_definitions[kind]
                    monsters.append(Monster(name=monster_info['name'], x=x, y=y, **monster_definition))
        return cls(identifier=identifier, monsters=monsters)

    @staticmethod
    def _load_environment_from_map(identifier: str) -> Tuple[List[Obstacle], List[Walkable]]:
        obstacles = []
        walkables = []
        world_map, map_legend = read_map(identifier)
        for y, row in enumerate(world_map):
            for x, cell_char in enumerate(row):
                try:
                    cell_info = map_legend[cell_char]
                except KeyError as e:
                    raise KeyError(f'Map character {cell_char} is not defined in map_legend') from e
                tile = cell_info['tile']
                if tile == constants.OBSTACLE:
                    obstacles.append(Obstacle(x=x, y=y))
                elif tile == constants.WALKABLE:
                    walkables.append(Walkable(x=x, y=y))
                else:
                    raise ValueError(f'Tile {tile} is neither obstacle nor walkable')
        return obstacles, walkables
