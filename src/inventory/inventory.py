import os.path
from importlib import import_module
from typing import Type, Dict, TypedDict

import pygame

import constants


class InventoryDict(TypedDict):
    """
    JSON representation of an inventory object's state
    """

    identifier: str
    name: str
    value: int


class InventoryObject:
    IMAGE_DIR: str = os.path.join(constants.DATA_DIR, 'images', 'inventory')

    # To be defined by concrete implementations
    IMAGE: str
    IDENTIFIER: str

    _identifier_to_klass: Dict[str, Type['InventoryObject']] = {}

    def __init__(self, name: str, value: int, **kwargs):
        self.name: str = name
        self.value: int = value
        self.image: pygame.Surface = self._load_image(self.IMAGE)

    @classmethod
    def register(cls, identifier: str, klass: Type['InventoryObject']):
        """
        Class method to be called in the modules where the concrete inventory objects are implemented
        """

        cls._identifier_to_klass[identifier] = klass

    @classmethod
    def from_json(cls, data: InventoryDict, **kwargs) -> 'InventoryObject':
        identifier = data['identifier']
        try:
            klass = cls._identifier_to_klass[identifier]
            return klass(**data, **kwargs)
        except KeyError:
            raise AssertionError(f'Inventory object {identifier} is not registered')

    def as_json(self) -> InventoryDict:
        # noinspection PyUnresolvedReferences
        return {
            field: getattr(self, field)
            for field in InventoryDict.__required_keys__
        }

    def _load_image(self, image_name: str) -> pygame.Surface:
        filepath = os.path.join(self.IMAGE_DIR, image_name)
        try:
            return pygame.image.load(filepath).convert_alpha()
        except Exception as e:
            s = f'Couldn\'t open {filepath}: {e}'
            raise ValueError(s) from e

    def __str__(self):
        return self.name


dirname = os.path.dirname(__file__)
modules = os.scandir(dirname)
for module in modules:
    if module.name.startswith('__') or module.name == 'monster.py':
        continue
    module_name = os.path.splitext(module.name)[0]
    import_module(f'monster.{module_name}')
