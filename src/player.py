from typing import List, TypedDict

import constants
from creature import Creature, CreatureDict
from environment import Obstacle
from tile import OrientedTile
from utils import Direction, convert_direction_to_dx_dy
from zonemap import ZoneMap


class PlayerDict(CreatureDict):
    """
    JSON representation of a _player's state
    """

    pass


class Player(OrientedTile, Creature):
    IMAGE = constants.PLAYER_IMG
    IMAGE_DEAD = constants.PLAYER_IMG_DEAD

    def move(self, direction: Direction, zone_map: ZoneMap):
        if self.is_dead():
            print('You cannot move when you are dead')
            return

        # First rotate the image, then move the iamge
        self.orient_towards(direction)
        dx, dy = convert_direction_to_dx_dy(direction)
        if zone_map.tile_is_walkable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
