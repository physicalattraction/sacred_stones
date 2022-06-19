from inventory.inventory import InventoryObject
from inventory.weapon import Weapon


class Dagger(Weapon):
    IMAGE = 'dagger.png'
    IDENTIFIER = 'dagger'

    def __init__(self, name: str = 'Dagger', value: int = 100, **kwargs):
        super().__init__(name=name, value=value, **kwargs)


InventoryObject.register(Dagger.IDENTIFIER, Dagger)
