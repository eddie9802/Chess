import Board
import pkg_resources.py2_warn
import pygame
import Draw
import ptext
from Colour import Colour

import math
from time import sleep


HEIGHT = 800
WIDTH = 800
LEFT = 1
RIGHT = 3
GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


def game_loop():
    global GAME_DISPLAY
    global HEIGHT
    global WIDTH
    pygame.init()
    Board.init(GAME_DISPLAY)
    pygame.display.set_caption('My Chess')
    clock = pygame.time.Clock()
    hasQuit = False
    while not hasQuit:
        pygame.display.update()
        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == pygame.QUIT:
                hasQuit = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                pos = pygame.mouse.get_pos()
                Board.select_square(pos)
                if Board.check_for_checkmate():
                    if Board.turn != Colour.WHITE:
                        ptext.draw("White wins!", (20, (HEIGHT / 2) - (HEIGHT / 8)), fontsize = HEIGHT / 8, color=(255, 0, 0))
                    else:
                        ptext.draw("Black wins!", (20, (HEIGHT / 2) - (HEIGHT / 8)), fontsize = HEIGHT / 8, color=(255, 0, 0))
                    Board.GAME_FINISHED = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                pos = pygame.mouse.get_pos()
                Board.promote_pawn(pos)
                Board.castle(pos)


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Draw.remove_all_highlights(GAME_DISPLAY)
                    Draw.remove_selection(GAME_DISPLAY)

            elif event.type == pygame.VIDEORESIZE:
                length = min(event.size)
                HEIGHT = length
                WIDTH = length
                Board.sqr_length = math.floor(length / 8)
                GAME_DISPLAY = pygame.display.set_mode((length, length), pygame.RESIZABLE)
                Board.GAME_DISPLAY = GAME_DISPLAY #  Sets the game display to the newly resized game display
                Draw.redraw_board(GAME_DISPLAY)

        clock.tick(30)


if __name__ == "__main__":
    game_loop()