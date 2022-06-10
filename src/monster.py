import json
import os.path
from typing import TypedDict

import constants
from creature import Creature, CreatureDict

MONSTER_DEFINITION_FILE = os.path.join(constants.DATA_DIR, 'creatures', 'monsters.json')


class MonsterDefinition(TypedDict):
    """
    JSON representation of a _monster's properties at initialization
    """

    # TODO: Make a Python class per _monster?

    kind: str
    armor: int
    max_damage: int
    chance_to_hit: int
    max_hit_points: int


class MonsterDict(CreatureDict):
    """
    JSON representation of a _monster's state
    """

    pass


class Monster(Creature):
    IMAGE = constants.MONSTER_IMG
    IMAGE_DEAD = constants.MONSTER_IMG_DEAD


with open(MONSTER_DEFINITION_FILE, 'r') as f:
    print('Reading monster definition file')
    monster_definitions = json.load(f)
