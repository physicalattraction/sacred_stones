from typing import List, TypedDict

import constants
from creature import Creature, CreatureDict
from tiles import OrientedTile, Obstacle
from utils import Direction, convert_direction_to_dx_dy


class PlayerDict(CreatureDict):
    """
    JSON representation of a player's state
    """

    pass


class Player(OrientedTile, Creature):
    IMAGE = constants.PLAYER_IMG
    IMAGE_DEAD = constants.PLAYER_IMG_DEAD

    def move(self, direction: Direction, obstacles: List[Obstacle]):
        if self.is_dead():
            print('You cannot move when you are dead')
            return

        # First rotate the image, then move the iamge
        self.orient_towards(direction)
        dx, dy = convert_direction_to_dx_dy(direction)
        if not self._collide_with_obstacles(dx, dy, obstacles):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)

    def _collide_with_obstacles(self, dx: int, dy: int, obstacles: List[Obstacle]) -> bool:
        return any(obstacle.x == self.x + dx and obstacle.y == self.y + dy for obstacle in obstacles)
