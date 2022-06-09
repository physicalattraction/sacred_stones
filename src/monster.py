import json
from typing import TypedDict

import constants
from creature import Creature, CreatureDict


class MonsterDefinition(TypedDict):
    """
    JSON representation of a monster's properties at initialization
    """

    # TODO: Make a Python class per monster?

    kind: str
    armor: int
    max_damage: int
    chance_to_hit: int
    max_hit_points: int


class MonsterDict(CreatureDict):
    """
    JSON representation of a monster's state
    """

    pass


class Monster(Creature):
    IMAGE = constants.MONSTER_IMG
    IMAGE_DEAD = constants.MONSTER_IMG_DEAD


with open(constants.MONSTER_DEFINITION_FILE, 'r') as f:
    print('Reading monster definition file')
    monster_definitions = json.load(f)
