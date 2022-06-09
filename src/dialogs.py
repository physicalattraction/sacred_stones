import random

import pygame

import constants
import utils
from monster import Monster
from player import Player


class TextDialog:
    def __init__(self, text, line_width=50):
        self.BG_COLOR = constants.LIGHTGREY
        self.text_list = []
        if type(text) == type("abc"):
            self.text_list = utils.separate_text_into_lines(text, line_width)
        elif type(text) == type([]):
            for elem in text:
                temp = utils.separate_text_into_lines(elem, line_length=100)
                for line in temp:
                    self.text_list.append(line)
                # self.text_list.append(temp)
        else:
            s = "Doh! That type of data shouldn't be here!"
            raise ValueError(s)
        # -------------------------
        if len(self.text_list) > 12:
            s = "Error! Textbox should not contain more than 12 lines."
            raise ValueError(s)
        # -------------------------
        pygame.init()
        self.font = pygame.font.Font(None, 35)
        # -------------------------
        text_width, text_height = self.font.size("a")
        self.width = 50 * text_width
        self.height = 400
        kind = ""
        self.screen = pygame.display.set_mode((self.width, self.height))
        # ----
        self.line_height = -1
        for elem in self.text_list:
            try:
                text_width, text_height = self.font.size(elem)
            except:
                try:
                    text_width, text_height = self.font.size(elem[0])
                except:
                    raise ValueError("Error!")
            if text_height > self.line_height:
                self.line_height = text_height
        # -------------------------
        # ----- Text Window -------
        window_left = 10
        window_top = 10
        window_width = self.width - 20
        window_height = self.height - (20 * 3)
        self.window_rect = pygame.Rect(window_left, window_top, window_width, window_height)
        # --------------------------
        # -------- OK Button -------
        button_width = 60
        button_height = 35
        button_left = int(self.height / 2)
        top = 600 - button_height
        self.okay_rect = pygame.Rect(button_left, top, button_width, button_height)
        # else:
        #     raise ValueError("I don't recognize that: ", kind)
        # -------------------------
        self.mouse_pos = None
        self.keep_looping = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                if event.key == pygame.K_RETURN:
                    self.keep_looping = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
                elif mouse_pressed[2] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()

    def _draw_lines(self):
        # karen
        for count, elem in enumerate(self.text_list):
            try:
                surface = self.font.render(elem, True, (0, 0, 0))
            except:
                try:
                    surface = self.font.render(elem[0], True, (0, 0, 0))
                except:
                    raise ValueError("Error!")
            # ----------------------
            left = 20
            top = (self.line_height * count) + 20
            # ----------------------
            self.screen.blit(surface, (left, top), area=None)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        pygame.draw.rect(self.screen, constants.WHITE, self.window_rect)
        pygame.draw.rect(self.screen, constants.PURPLE, self.okay_rect)
        self._draw_lines()

        # Render the text used to label the button
        surface = self.font.render("OK", True, constants.BLACK)
        self.screen.blit(surface, self.okay_rect)

        if self.mouse_pos is not None:
            okay_result = self.okay_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            self.mouse_pos = None
            if okay_result == 1:
                self.message = ""
                self.keep_looping = False

        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.events()
            self.draw()


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
                    self.player.hit_points -= 2
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
