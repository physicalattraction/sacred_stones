import os.path
import random
from typing import List

import pygame

import constants
import utils
from monster import Monster
from player import Player


class Fight:
    """
    Take the player and a monster and let them fight
    """

    BACKROUND_IMAGE_DIR = os.path.join(constants.DATA_DIR, 'images', 'background', 'fight')
    FLEE_PENALTY = 20

    def __init__(self, player: Player, monster: Monster):
        self._screen = utils.init_pygame()

        background_image_filepath = os.path.join(self.BACKROUND_IMAGE_DIR, self._get_random_background_image())

        self._background_image = pygame.image.load(background_image_filepath)
        self._player = player
        self._monster = monster
        self._all_sprites = pygame.sprite.Group(self._player, self._monster)
        self._keep_looping = True

        self._font = pygame.font.Font(None, 35)
        self._clock = pygame.time.Clock()

        multiplier = 4  # Make the image 4 times bigger as on the zone map
        self._player.place_on_screen(constants.TILESIZE * multiplier, 0, 0)
        self._monster.place_on_screen(constants.TILESIZE * multiplier, constants.NR_BLOCKS_WIDE // multiplier - 1, 0)

    def _get_background_images(self) -> List[str]:
        """
        Filenames of possible background images
        """

        return list(os.scandir(self.BACKROUND_IMAGE_DIR))

    def _get_random_background_image(self) -> str:
        bg_images = self._get_background_images()
        rand_int = random.randint(0, len(bg_images) - 1)
        return bg_images[rand_int]

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_x):
                    self._player_flees()
                elif event.key == pygame.K_h:
                    self._player_attacks_monster()
                    self._monster_attacks_player()
                else:
                    pass

    def _player_flees(self):
        print(f'{self._player} flees from {self._monster}')
        self._player.hit_points -= self.FLEE_PENALTY
        self._keep_looping = False

    def _player_attacks_monster(self):
        roll_of_dice = random.randint(0, 99)
        if roll_of_dice <= self._player.chance_to_hit:
            self._monster.hit_points -= self._player.calculate_damage(self._monster)
        if self._monster.is_dead():
            print(f'{self._player} killed {self._monster}')
            self._keep_looping = False

    def _monster_attacks_player(self):
        roll_of_dice = random.randint(0, 99)
        if roll_of_dice <= self._monster.chance_to_hit:
            self._player.hit_points -= self._monster.calculate_damage(self._player)
        elif self._player.is_dead():
            print(f'{self._player} is killed by {self._monster}')
            self._keep_looping = False

    def _draw(self):
        self._screen.blit(self._background_image, (0, 0))

        monster_list = [f'{str(self._monster).title()}:', f'Hit Points: {self._monster.hit_points}',
                        f'Armor: {self._monster.armor}', f'Max damage: {self._monster.max_damage}',
                        f'Chance to hit: {self._monster.chance_to_hit}']
        utils.display_text(self._screen, monster_list, self._font, width_offset=475,
                           height_offset=250, line_width=60, color=constants.YELLOW, shadow_color=constants.BLACK)

        player_list = [f'{self._player}:', f'Hit Points: {self._player.hit_points}', f'Armor: {self._player.armor}',
                       f'Max damage: {self._player.max_damage}', f'Chance to hit: {self._player.chance_to_hit}']
        player_height = utils.display_text(self._screen, player_list, self._font, width_offset=20,
                                           height_offset=250, line_width=60,
                                           color=constants.YELLOW, shadow_color=constants.BLACK)

        action_list = ['What would you like to do?', 'H = Hit',
                       f'X = Flee (Fleeing will cost {self.FLEE_PENALTY} hitpoints)']
        utils.display_text(self._screen, action_list, self._font, width_offset=20,
                           height_offset=250 + player_height + 40, line_width=60,
                           color=constants.YELLOW, shadow_color=constants.BLACK)

        self._all_sprites.update()
        self._all_sprites.draw(self._screen)
        pygame.display.flip()

    def main(self):
        self._clock.tick(constants.FRAME_RATE)
        while self._keep_looping:
            self._handle_events()
            self._draw()
