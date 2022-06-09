import json
import os.path
import shutil
import sys
from shutil import copyfile
from typing import Optional, List, TypedDict

import pygame

import constants
from constants import DATA_DIR
from dialogs import TextDialog, DialogFight
from map import read_map
from monster import Monster
from tiles import Player, Obstacle, Walkable
from zone import Zone


# Game state dicts

class PlayerDict(TypedDict):
    name: str
    kind: str
    x: int
    y: int
    armor: int
    max_damage: int
    chance_to_hit: int
    max_hit_points: int
    hit_points: int


class GameDataDict(TypedDict):
    active_zone: str
    player: PlayerDict


class Game:
    _keep_looping: bool
    _active_zone: str
    _obstacles: List[Obstacle]
    _walkables: List[Walkable]
    _player: Player
    _all_sprites: Optional[pygame.sprite.Group]

    def __init__(self):
        # Lazy loading backing variables
        self._init_pygame()

        self.display_surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.display_surface.fill(constants.UGLY_PINK)

        self.restart_game()

    def _init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(constants.TITLE)
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.font = pygame.font.Font(None, 40)

    @property
    def all_sprites(self) -> pygame.sprite.Group:
        if not self._all_sprites:
            self._all_sprites = pygame.sprite.Group()
            for elem in self._walkables:
                self._all_sprites.add(elem)
            for elem in self._obstacles:
                self._all_sprites.add(elem)
            for monster in self._zone.monsters:
                self._all_sprites.add(monster)
            self._all_sprites.add(self._player)
        return self._all_sprites

    def _load_environment_from_map(self):
        self._obstacles = []
        self._walkables = []
        world_map, map_legend = read_map(self._active_zone)
        for y, row in enumerate(world_map):
            for x, cell_char in enumerate(row):
                try:
                    cell_info = map_legend[cell_char]
                except KeyError as e:
                    raise KeyError(f'Map character {cell_char} is not defined in map_legend') from e
                tile = cell_info['tile']
                if tile == constants.OBSTACLE:
                    self._obstacles.append(Obstacle(x=x, y=y))
                elif tile == constants.WALKABLE:
                    self._walkables.append(Walkable(x=x, y=y))
                else:
                    raise ValueError(f'Tile {tile} is neither obstacle nor walkable')

    def _load_game_data(self):
        if not os.path.isfile(constants.CURRENT_GAME_FILE):
            copyfile(constants.ORIGINAL_GAME_FILE, constants.CURRENT_GAME_FILE)
        with open(constants.CURRENT_GAME_FILE, 'r') as f:
            game_data = json.load(f)
        self._active_zone = game_data['active_zone']
        self._player = Player.from_json(game_data['player'])
        self._zone = Zone.load(self._active_zone)

    def _save_game_data(self):
        # TODO: Implement a as_json method
        # TODO: Make a helper class (ABC) for this loading and saving
        game_data = {'active_zone': self._active_zone,
                     'player': self._player.as_json()}
        with open(constants.CURRENT_GAME_FILE, 'w') as f:
            json.dump(game_data, f, indent=2)
        self._zone.save()

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
                    self.restart_game()
                if event.key == pygame.K_LEFT:
                    self._player.move(direction=constants.LEFT, obstacles=self._obstacles)
                elif event.key == pygame.K_RIGHT:
                    self._player.move(direction=constants.RIGHT, obstacles=self._obstacles)
                elif event.key == pygame.K_DOWN:
                    self._player.move(direction=constants.DOWN, obstacles=self._obstacles)
                elif event.key == pygame.K_UP:
                    self._player.move(direction=constants.UP, obstacles=self._obstacles)
                elif event.key == pygame.K_h:
                    monster = self.monster_on_tile(self._player.x, self._player.y)
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
                self._save_game_data()

    def draw_stuff(self):
        self.all_sprites.update()
        self.all_sprites.draw(self.display_surface)

    def quit(self):
        pygame.quit()
        sys.exit()

    def monster_on_tile(self, x: int, y: int) -> Optional[Monster]:
        """
        Return the monster on the given tile, or None if there is no monster on the tile
        """

        # TODO: Delegate to Zone?

        return next((monster for monster in self._zone.monsters if monster.x == x and monster.y == y), None)

    def dialog_have_a_fight(self, monster):
        fight_dialog = DialogFight(self._player, monster)
        fight_dialog.main()
        self._save_game_data()
        self.restart_game()

    def restart_game(self):
        self._init_pygame()
        self._all_sprites = None
        self._keep_looping = True
        self._load_game_data()
        self._load_environment_from_map()

    def player_died(self):
        s = 'You are dead! Game over.'
        mydialog = TextDialog(s)
        mydialog.main()
        self._keep_looping = False
        self._init_pygame()
        # TODO: Restart game from latest savegame when player dies
