import json
import os.path
from typing import List, TypedDict

from constants import DATA_DIR
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
    monsters: List[Monster]

    def __init__(self, identifier: str, monsters: List[Monster]):
        self.identifier = identifier
        self.monsters = monsters

    @classmethod
    def get_filepath(cls, identifier: str):
        # TODO: Remove hardcoded current when implementing save slots
        return os.path.join(DATA_DIR, 'current', 'zones', f'{identifier}.json')

    @classmethod
    def from_json(cls, data: ZoneDict):
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
