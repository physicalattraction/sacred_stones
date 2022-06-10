import random

import pygame

import constants
import utils
from monster import Monster
from player import Player


class Fight:
    """
    Takes the _player and a _monster and lets them fight
    """

    BG_COLOR = constants.WHITE
    FLEE_PENALTY = 20

    def __init__(self, player: Player, monster: Monster):
        self._screen = utils.init_pygame()
        self._player = player
        self._monster = monster
        self._all_sprites = pygame.sprite.Group(self._player, self._monster)
        self._keep_looping = True

        self._font = pygame.font.Font(None, 35)
        self._clock = pygame.time.Clock()

        multiplier = 4  # Make the image 4 times bigger as on the zone map
        self._player.place_on_screen(constants.TILESIZE * multiplier, 0, 0)
        self._monster.place_on_screen(constants.TILESIZE * multiplier, constants.NR_BLOCKS_WIDE // multiplier - 1, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_x):
                    print(f'Player flees from {self._monster.name}')
                    self._player.hit_points -= self.FLEE_PENALTY
                    self._keep_looping = False
                elif event.key == pygame.K_h:
                    myran = random.randint(0, 99)
                    if myran <= self._player.chance_to_hit:
                        self._monster.hit_points -= self._player.calculate_damage(self._monster)
                    myran = random.randint(0, 99)
                    if myran <= self._monster.chance_to_hit:
                        self._player.hit_points -= self._monster.calculate_damage(self._player)
                    if self._monster.hit_points <= 0:
                        self._keep_looping = False
                    elif self._player.hit_points <= 0:
                        self._keep_looping = False
                else:
                    pass

    def draw(self):
        self._screen.fill(self.BG_COLOR)

        monster_list = [f'{self._monster.kind.capitalize()} hit points:', f'hp: {self._monster.hit_points}']
        utils.talk_dialog(self._screen, monster_list, self._font, width_offset=475, height_offset=250, line_width=60,
                          color=constants.BLACK)
        # ----
        player_list = ['Player hit points:', f'hp: {self._player.hit_points}']
        utils.talk_dialog(self._screen, player_list, self._font, width_offset=20, height_offset=250, line_width=60,
                          color=constants.BLACK)
        # ----
        action_list = ['What would you like to do?', 'H = Hit', 'X = Flee (Fleeing will cost 2 hitpoints)']
        utils.talk_dialog(self._screen, action_list, self._font, width_offset=20, height_offset=350, line_width=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self._all_sprites.update()
        self._all_sprites.draw(self._screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self._clock.tick(constants.FRAME_RATE)
        while self._keep_looping:
            self.handle_events()
            self.draw()
        # TODO: Don't call private methods in this dialog, and especially not in main
        self._monster.image = self._monster._load_image(self._monster.image_name)
        self._monster.place_on_screen(constants.TILESIZE, self._monster.x, self._monster.y)
