import json
import os.path
import shutil
import sys
from shutil import copyfile
from typing import Optional, List, TypedDict, Dict

import pygame

import constants
from constants import DATA_DIR
from fight import Fight
from text_dialog import TextDialog
from player import Player, PlayerDict
from saveable import Saveable
from environment import Obstacle, Walkable
from utils import init_pygame
from zone import Zone


class GameDict(TypedDict):
    active_zone: str
    player: PlayerDict


class Game(Saveable):
    _keep_looping: bool
    _active_zone: str
    _player: Player
    _zone: Zone
    _obstacles: List[Obstacle]
    _walkables: List[Walkable]
    _all_sprites: Optional[pygame.sprite.Group]

    def __init__(self):
        init_pygame()
        self._all_sprites = None
        self._keep_looping = True
        self._display_surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self._display_surface.fill(constants.UGLY_PINK)

        self._resume()

    @property
    def all_sprites(self) -> pygame.sprite.Group:
        # TODO: Let zones define their own all sprites
        if not self._all_sprites:
            self._all_sprites = pygame.sprite.Group(*self._zone.all_sprites, self._player)
            # self._all_sprites = pygame.sprite.Group()
            # self._all_sprites_2 = pygame.sprite.Group()
            # for elem in self._zone.walkables:
            #     self._all_sprites.add(elem)
            # for elem in self._zone.obstacles:
            #     self._all_sprites.add(elem)
            # for _monster in self._zone.monsters:
            #     self._all_sprites.add(_monster)
            # self._all_sprites.add(self._player)
        return self._all_sprites

    # Saveable methods

    @classmethod
    def from_json(cls, data: Dict) -> 'Game':
        game = cls()
        game._set_data(data)
        return game

    def as_json(self) -> GameDict:
        return {'active_zone': self._active_zone, 'player': self._player.as_json()}

    @classmethod
    def load(cls):
        data = cls._get_saved_data()
        return cls.from_json(data)

    def save(self):
        with open(constants.CURRENT_GAME_FILE, 'w') as f:
            json.dump(self.as_json(), f, indent=2)
        self._zone.save()

    # Public methods

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                    return True
                if event.key == pygame.K_r:
                    # TODO: This should not be so easy, but good for debugging
                    print('Restart')
                    os.remove(constants.CURRENT_GAME_FILE)
                    shutil.rmtree(os.path.join(DATA_DIR, 'current', 'zones'))
                    os.mkdir(os.path.join(DATA_DIR, 'current', 'zones'))
                    self._resume()
                if event.key == pygame.K_LEFT:
                    # TODO: Continue from here: use Map.is_walkable
                    self._player.move(direction=constants.LEFT, zone_map=self._zone.map)
                elif event.key == pygame.K_RIGHT:
                    self._player.move(direction=constants.RIGHT, zone_map=self._zone.map)
                elif event.key == pygame.K_DOWN:
                    self._player.move(direction=constants.DOWN, zone_map=self._zone.map)
                elif event.key == pygame.K_UP:
                    self._player.move(direction=constants.UP, zone_map=self._zone.map)
                elif event.key == pygame.K_h:
                    monster = self._zone.monster_on_tile(self._player.x, self._player.y)
                    if not monster:
                        print('Player swings at the air')
                        return False
                    if monster.is_dead():
                        print('Monster is already dead')
                        return False
                    print('Fight!!!')
                    self.dialog_have_a_fight(monster)
                    if self._player.is_dead():
                        self.player_died()
                self.save()

    @staticmethod
    def _get_saved_data() -> GameDict:
        """
        Get the data saved in `current`, or from original if there is no current Game info
        """

        if not os.path.isfile(constants.CURRENT_GAME_FILE):
            copyfile(constants.ORIGINAL_GAME_FILE, constants.CURRENT_GAME_FILE)
        with open(constants.CURRENT_GAME_FILE, 'r') as f:
            return json.load(f)

    def _set_data(self, data: GameDict) -> None:
        """
        Set the given data in this Game instance
        """

        self._active_zone = data['active_zone']
        self._player = Player.from_json(data['player'])
        self._zone = Zone.load(data['active_zone'])

    def draw_stuff(self):
        self.all_sprites.update()
        self.all_sprites.draw(self._display_surface)

    def quit(self):
        pygame.quit()
        sys.exit()

    def dialog_have_a_fight(self, monster):
        fight_dialog = Fight(self._player, monster)
        fight_dialog.main()
        self.save()
        self._resume()

    def _resume(self):
        init_pygame()
        self._all_sprites = None
        self._keep_looping = True
        data = self._get_saved_data()
        self._set_data(data)

    def player_died(self):
        TextDialog.show('You are dead! Game over.')
        self._keep_looping = False
        init_pygame()
        # TODO: Restart game from latest savegame when _player dies
