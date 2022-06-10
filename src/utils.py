from typing import Tuple, List, Union

import pygame

import constants

Direction = int


# Helper methods

def init_pygame(title: str = constants.TITLE, width: int = constants.SCREEN_WIDTH,
                height: int = constants.SCREEN_HEIGHT) -> pygame.Surface:
    pygame.init()
    pygame.display.set_caption(title)
    return pygame.display.set_mode((width, height))


def convert_direction_to_dx_dy(direction: Direction) -> Tuple[int, int]:
    """
    Convert the direction into a tuple of movement in x and y direction
    """

    if direction == constants.LEFT:
        return -1, 0
    if direction == constants.RIGHT:
        return 1, 0
    if direction == constants.DOWN:
        return 0, 1
    if direction == constants.UP:
        return 0, -1


def get_text_list(text: Union[str, List[str]], line_width: int) -> List[str]:
    """
    Separate a text into a list of texts with maximum length of line_width

    If the input is a list, the line breaks are kept, but still split if too long

    >>> get_text_list('Hello world', 2)
    ['He', 'll', 'o', 'wo', 'rl', 'd']
    >>> get_text_list('Hello world', 5)
    ['Hello', 'world']
    >>> get_text_list('Hello world', 8)
    ['Hello', 'world']
    >>> get_text_list('Hello world', 12)
    ['Hello world']
    >>> get_text_list('Hello world', 3)
    ['Hel', 'lo', 'wor', 'ld']
    >>> get_text_list(['Hello', 'world'], 12)
    ['Hello', 'world']
    """

    def _separate_text_into_lines(_text: str) -> List[str]:
        _result = []
        while len(_text) >= line_width:
            index_of_last_space = _text[0:line_width].rfind(' ')
            if index_of_last_space == -1:
                index_of_last_space = line_width
            _result.append(_text[0:index_of_last_space].strip())
            _text = _text[index_of_last_space:].strip()
        if _text:
            _result.append(_text)
        return _result

    if isinstance(text, str):
        result = _separate_text_into_lines(text)
    elif isinstance(text, list):
        # Keep the original line breaks, but break long lines up.
        result = []
        for line in text:
            result += _separate_text_into_lines(line)
    else:
        s = f'Expected a str or list of str, given {type(text)}'
        raise ValueError(s)
    return result



def _top_height(text_list, font):
    if not isinstance(text_list, list):
        raise ValueError('Error')
    tallest = -1
    for elem in text_list:
        try:
            _, text_height = font.size(elem)
        except:
            raise ValueError(elem)
        if text_height > tallest:
            tallest = text_height
    return tallest


def talk_dialog(screen: pygame.Surface, text: Union[str, list], font: pygame.font.Font,
                width_offset: int, height_offset: int, line_width: int = 32,
                color: Tuple[int, int, int] = constants.BLACK):
    """
    Display the given text onto the given screen
    """

    text_list = get_text_list(text, line_width)

    # ----------------------
    text_height = _top_height(text_list, font) + 3
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        # ----------------------
        left = width_offset
        height = height_offset + (text_height * count)
        top = height + 10
        screen.blit(surface, (left, top))
