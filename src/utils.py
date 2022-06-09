from typing import Tuple

import constants

Direction = int


def convert_direction_to_dx_dy(direction: Direction) -> Tuple[int, int]:
    if direction == constants.LEFT:
        return -1, 0
    if direction == constants.RIGHT:
        return 1, 0
    if direction == constants.DOWN:
        return 0, 1
    if direction == constants.UP:
        return 0, -1


def separate_text_into_lines(mytext, line_length):
    mylist = []
    while len(mytext) >= line_length:
        int = mytext[0:line_length].rfind(' ')
        mylist.append(mytext[0:int].strip())
        mytext = mytext[int:].strip()
    mylist.append(mytext)
    return mylist


def _top_height(text_list, font):
    if not type(text_list) == type([]):
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
    # text_list = separate_text_into_lines(text, line_length)
    text_list = []
    if type(text) == type('bla'):
        text_list = separate_text_into_lines(text, line_length)
    elif type(text) == type([]):
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
