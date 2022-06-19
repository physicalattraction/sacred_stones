import os.path
import random
from importlib import import_module
from typing import Type, Dict, Union

import constants
from creature import Creature, CreatureDict
from zonemap import MonsterAssignment


class MonsterDict(CreatureDict):
    """
    JSON representation of a _monster's state
    """

    identifier: str


class Monster(Creature):
    IMAGE_DIR: str = os.path.join(constants.DATA_DIR, 'images', 'monster')
    NAMES = ['Monster']

    _identifier_to_klass: Dict[str, Type['Monster']] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = self._get_name()

    @classmethod
    def register(cls, identifier: str, klass: Type['Monster']):
        """
        Class method to be called in the modules where the concrete monsters are implemented
        """

        cls._identifier_to_klass[identifier] = klass

    @classmethod
    def from_json(cls, data: Union[MonsterDict, MonsterAssignment], **kwargs) -> 'Monster':
        identifier = data['identifier']
        try:
            klass = cls._identifier_to_klass[identifier]
            return klass(**data, **kwargs)
        except KeyError:
            raise AssertionError(f'Monster {identifier} is not registered')

    def as_json(self) -> MonsterDict:
        # noinspection PyUnresolvedReferences
        return {
            field: getattr(self, field)
            for field in MonsterDict.__required_keys__
        }

    @property
    def gold_when_killed(self) -> int:
        return 0

    @property
    def experience_when_killed(self) -> int:
        return 0

    def _get_name(self):
        return random.choice(self.NAMES)

    def __str__(self):
        return f'{self.kind} {self.name}'


dirname = os.path.dirname(__file__)
modules = os.scandir(dirname)
for module in modules:
    if module.name.startswith('__') or module.name == 'monster.py':
        continue
    module_name = os.path.splitext(module.name)[0]
    import_module(f'monster.{module_name}')
