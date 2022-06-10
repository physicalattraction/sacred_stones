import pygame

import constants
import utils


class TextDialog:
    """
    Class that displays a text message to the screen, with only an OK button
    """

    BG_COLOR = constants.LIGHT_GREY

    @staticmethod
    def show(msg: str):
        dialog = TextDialog(msg)
        dialog.main()

    def __init__(self, text: str, line_width: int = 50):
        pygame.init()
        self._font = pygame.font.Font(None, 35)

        self._set_text_list(text, line_width)

        # Make the screen 50 characters wide, regardless of the text, plus 40 pixels margin
        text_width, _ = self._font.size('a')
        self._screen_width = line_width * text_width + 40

        # Make the screen 80 pixels + the _screen_height needed for the text
        self._line_height = -1
        self._screen_height = 80
        for elem in self._text_list:
            _, text_height = self._font.size(elem)
            if text_height > self._line_height:
                self._line_height = text_height
            self._screen_height += text_height
        self.screen = pygame.display.set_mode((self._screen_width, self._screen_height))

        # The white window inside the grey window
        window_left = 10
        window_top = 10
        window_width = self._screen_width - 20
        window_height = self._screen_height - 60
        self._text_window_rect = pygame.Rect(window_left, window_top, window_width, window_height)

        button_width = 60
        button_height = 30
        button_left = self._screen_width - button_width - 20
        top = self._screen_height - button_height - 10
        self._okay_rect = pygame.Rect(button_left, top, button_width, button_height)

        self._mouse_pos = None
        self._keep_looping = True

    def _set_text_list(self, text, line_width):
        self._text_list = []
        if isinstance(text, str):
            self._text_list = utils.separate_text_into_lines(text, line_width)
        elif isinstance(text, list):
            # Keep the original line breaks, but break long lines up.
            self._text_list = []
            for elem in text:
                self._text_list += utils.separate_text_into_lines(elem, line_width)
        else:
            s = f'Can only init {self.__class__.__name__} with str or text, given {type(text)}'
            raise ValueError(s)
        if nr_lines := len(self._text_list) > 12:
            s = f'Textbox should not contain more than 12 lines, given {nr_lines}'
            raise ValueError(s)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._keep_looping = False
                if event.key == pygame.K_RETURN:
                    self._keep_looping = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
                if mouse_pressed[0] == 1:
                    self._mouse_pos = pygame.mouse.get_pos()
                elif mouse_pressed[2] == 1:
                    self._mouse_pos = pygame.mouse.get_pos()

    def _draw_lines(self):
        for count, elem in enumerate(self._text_list):
            surface = self._font.render(elem, True, (0, 0, 0))
            left = 20  # Left margin
            top = (self._line_height * count) + 20
            self.screen.blit(surface, (left, top), area=None)

    def _draw(self):
        self._draw_background()
        self._draw_lines()
        self._draw_button()

        if self._mouse_pos is not None:
            ok_is_clicked = self._okay_rect.collidepoint(self._mouse_pos[0], self._mouse_pos[1])
            if ok_is_clicked == 1:
                self._keep_looping = False

        pygame.display.flip()

    def _draw_button(self):
        surface = self._font.render('OK', True, constants.BLACK)
        width = surface.get_rect().width
        height = surface.get_rect().height
        left = self._okay_rect.left + (self._okay_rect.width - width) // 2  # Place text in center
        top = self._okay_rect.top + (self._okay_rect.height - height) // 2  # of the button
        self.screen.blit(surface, (left, top))

    def _draw_background(self):
        self.screen.fill(self.BG_COLOR)
        pygame.draw.rect(self.screen, constants.WHITE, self._text_window_rect)
        pygame.draw.rect(self.screen, constants.LIGHT_BLUE, self._okay_rect)

    def main(self):
        while self._keep_looping:
            self._handle_events()
            self._draw()
