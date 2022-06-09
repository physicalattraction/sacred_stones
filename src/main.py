# https://www.youtube.com/watch?v=MfoqWsTv1Wg&t=0s
# https://github.com/poly451/Tutorials/tree/master/Python:%20Create%20a%20Grid/Create%20a%20Grid%2004

import pygame

from game import Game


def run():
    game = Game.load()

    while True:
        game.handle_events()
        game.draw_stuff()
        pygame.display.update()


if __name__ == '__main__':
    run()
