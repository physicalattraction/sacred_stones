import json
import os.path
import sys
from shutil import copyfile
from typing import Optional, List, Tuple

import pygame

import constants
from dialogs import TextDialog, DialogFight
from tiles import Monster, Player, Obstacle, Walkable
from utils import DATA_DIR


class Game:
    _CURRENT_GAME_FILE = os.path.join(DATA_DIR, 'current', constants.GAME_DATA_FILE)

    _keep_looping: bool
    _zone: str
    _obstacles: List[Obstacle]
    _walkables: List[Walkable]
    _player: Player
    _monsters: List[Monster]
    _all_sprites: Optional[pygame.sprite.Group]

    def __init__(self):
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
            for monster in self._monsters:
                self._all_sprites.add(monster)
            self._all_sprites.add(self._player)
        return self._all_sprites

    def _load_tiles(self):
        self._obstacles = []
        self._walkables = []
        filepath = os.path.join(DATA_DIR, 'zones', self._zone, constants.MAPFILE)
        with open(filepath, 'r') as f:
            world_map = [i.strip() for i in f.readlines()]
        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == '1':
                    self._obstacles.append(Obstacle(x=row, y=col))
                elif tile == '.':
                    self._walkables.append(Walkable(x=row, y=col))
                elif tile == 'P':
                    self._walkables.append(Walkable(x=row, y=col))
                elif tile == 'M':
                    self._walkables.append(Walkable(x=row, y=col))

    def _load_game_data(self):
        if not os.path.isfile(self._CURRENT_GAME_FILE):
            src_filepath = os.path.join(DATA_DIR, 'original', constants.GAME_DATA_FILE)
            copyfile(src_filepath, self._CURRENT_GAME_FILE)
        with open(self._CURRENT_GAME_FILE, 'r') as f:
            game_data = json.load(f)
        self._zone = game_data['zone']
        self._player = Player.from_json(game_data['player'])
        self._monsters = [Monster.from_json(monster_data) for monster_data in game_data['monsters']]

    def _save_game_data(self):
        game_data = {'zone': self._zone,
                     'player': self._player.as_json(),
                     'monsters': [monster.as_json() for monster in self._monsters]}
        with open(self._CURRENT_GAME_FILE, 'w') as f:
            json.dump(game_data, f, indent=2)

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
                    os.remove(self._CURRENT_GAME_FILE)
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
                    print("Fight!!!")
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

        return next((monster for monster in self._monsters if monster.x == x and monster.y == y), None)

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
        self._load_tiles()

    def player_died(self):
        s = 'You are dead! Game over.'
        mydialog = TextDialog(s)
        mydialog.main()
        self._keep_looping = False
        self._init_pygame()
