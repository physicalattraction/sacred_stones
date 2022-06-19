from inventory.inventory import InventoryObject
from inventory.weapon import Weapon


class Sword(Weapon):
    IMAGE = 'sword.png'
    IDENTIFIER = 'sword'

    def __init__(self, **kwargs):
        super().__init__(name='Sword', value=200)


InventoryObject.register(Sword.IDENTIFIER, Sword)
