import random

import pygame

import constants
import utils
from monster import Monster
from player import Player



class DialogFight:
    """
    Takes the player and a monster and lets them fight
    """

    def __init__(self, player: Player, monster: Monster):
        self.player = player
        self.monster = monster
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        pygame.init()
        self.width = constants.WIDTH
        self.height = constants.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(constants.TITLE)
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text = ""
        self.input_text_color = constants.ORANGE
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        multiplier = 4
        self.player.place_on_screen(constants.TILESIZE * multiplier, 0, 0)
        self.monster.place_on_screen(constants.TILESIZE * multiplier, constants.NR_BLOCKS_WIDE // multiplier - 1, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_x):
                    print(f'Player flees from {self.monster.name}')
                    self.player.hit_points -= 20
                    self.keep_looping = False
                elif event.key == pygame.K_h:
                    myran = random.randint(0, 99)
                    if myran <= self.player.chance_to_hit:
                        self.monster.hit_points -= self.player.calculate_damage(self.monster)
                    myran = random.randint(0, 99)
                    if myran <= self.monster.chance_to_hit:
                        self.player.hit_points -= self.monster.calculate_damage(self.player)
                    if self.monster.hit_points <= 0:
                        self.keep_looping = False
                    elif self.player.hit_points <= 0:
                        self.keep_looping = False
                else:
                    pass

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.monster)
        # -----------------------------------------
        monster_list = [f'{self.monster.kind.capitalize()} hit points:', f'hp: {self.monster.hit_points}']
        utils.talk_dialog(self.screen, monster_list, self.font, width_offset=475, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        player_list = ['Player hit points:', f'hp: {self.player.hit_points}']
        utils.talk_dialog(self.screen, player_list, self.font, width_offset=20, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        action_list = ['What would you like to do?', 'H = Hit', 'X = Flee (Fleeing will cost 2 hitpoints)']
        utils.talk_dialog(self.screen, action_list, self.font, width_offset=20, height_offset=350, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # TODO: Don't call private methods in this dialog, and especially not in main
        self.monster.image = self.monster._load_image(self.monster.image_name)
        self.monster.place_on_screen(constants.TILESIZE, self.monster.x, self.monster.y)
