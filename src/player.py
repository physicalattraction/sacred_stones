import os.path

import constants
from creature import Creature, CreatureDict
from tile import OrientedTile
from utils import Direction, convert_direction_to_dx_dy
from zonemap import ZoneMap, WEST, EAST, NORTH, SOUTH


class PlayerDict(CreatureDict):
    """
    JSON representation of a _player's state
    """

    direction: int


class Player(OrientedTile, Creature):
    IMAGE_DIR: str = os.path.join(constants.DATA_DIR, 'images', 'player')
    IMAGE = constants.PLAYER_IMG
    IMAGE_DEAD = constants.PLAYER_IMG_DEAD

    def move(self, direction: Direction, zone_map: ZoneMap):
        if self.is_dead():
            print('You cannot move when you are dead')
            return

        # First rotate the image, then move the iamge
        self.orient_towards(direction)
        dx, dy = convert_direction_to_dx_dy(direction)
        if self.x + dx < 0:
            zone_to_move_to = zone_map.neighbor_zones[WEST]
            self.x = constants.NR_BLOCKS_WIDE - 1
            self.rect = self.rect.move((constants.NR_BLOCKS_WIDE - 1) * constants.TILESIZE, 0)
            print(f'Move WEST to {self.x}, {self.y} on {zone_to_move_to}')
            return zone_to_move_to
        if self.x + dx >= constants.NR_BLOCKS_WIDE:
            zone_to_move_to = zone_map.neighbor_zones[EAST]
            self.x = 0
            self.rect = self.rect.move(-(constants.NR_BLOCKS_HIGH - 1) * constants.TILESIZE, 0)
            print(f'Move EAST to {self.x}, {self.y} on {zone_to_move_to}')
            return zone_to_move_to
        if self.y + dy < 0:
            zone_to_move_to = zone_map.neighbor_zones[NORTH]
            self.y = constants.NR_BLOCKS_HIGH - 1
            self.rect = self.rect.move(0, (constants.NR_BLOCKS_HIGH - 1) * constants.TILESIZE)
            print(f'Move NORTH to {self.x}, {self.y} on {zone_to_move_to}')
            return zone_to_move_to
        if self.y + dy >= constants.NR_BLOCKS_HIGH:
            zone_to_move_to = zone_map.neighbor_zones[SOUTH]
            self.y = 0
            self.rect = self.rect.move(0, -(constants.NR_BLOCKS_HIGH - 1) * constants.TILESIZE)
            print(f'Move SOUTH to {self.x}, {self.y} on {zone_to_move_to}')
            return zone_to_move_to
        elif zone_map.tile_is_walkable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)

    def as_json(self) -> PlayerDict:
        # noinspection PyUnresolvedReferences
        return {
            field: getattr(self, field)
            for field in PlayerDict.__required_keys__
        }

    def __str__(self):
        return self.name
