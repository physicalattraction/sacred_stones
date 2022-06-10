from typing import Tuple, List

import constants

Direction = int


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


def separate_text_into_lines(txt: str, line_width: int) -> List[str]:
    """
    Separate a text into a list of text with maximum length of line_width

    >>> separate_text_into_lines('Hello world', 2)
    ['He', 'll', 'o', 'wo', 'rl', 'd']
    >>> separate_text_into_lines('Hello world', 5)
    ['Hello', 'world']
    >>> separate_text_into_lines('Hello world', 8)
    ['Hello', 'world']
    >>> separate_text_into_lines('Hello world', 12)
    ['Hello world']
    """

    result = []
    while len(txt) >= line_width:
        index_of_last_space = txt[0:line_width].rfind(' ')
        if index_of_last_space == -1:
            index_of_last_space = line_width
        result.append(txt[0:index_of_last_space].strip())
        txt = txt[index_of_last_space:].strip()
    if txt:
        result.append(txt)
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


def talk_dialog(screen, text, font, width_offset, height_offset, line_length=32, color=(0, 0, 0)):
    # _text_list = separate_text_into_lines(text, line_width)
    text_list = []
    if isinstance(text, str):
        text_list = separate_text_into_lines(text, line_length)
    elif isinstance(text, list):
        for line in text:
            temp = separate_text_into_lines(line, line_length)
            text_list += temp
    else:
        s = 'Doh! That type of data should not be here!'
        raise ValueError(s)
    # ----------------------
    text_height = _top_height(text_list, font) + 3
    for count, elem in enumerate(text_list):
        surface = font.render(elem, True, color)
        # ----------------------
        left = width_offset
        height = height_offset + (text_height * count)
        top = height + 10
        screen.blit(surface, (left, top))
