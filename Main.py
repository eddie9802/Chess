import Board
import pkg_resources.py2_warn
import pygame
import Draw
import ptext
from Colour import Colour
from Window import Window
import MainMenu
from PieceType import PieceType

import math
from time import sleep


HEIGHT = 800
WIDTH = 800
LEFT = 1
RIGHT = 3
GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
CURRENT_WINDOW = Window.MAIN_MENU

def resize_screen(event):
    length = min(event.size)
    HEIGHT = length
    WIDTH = length
    GAME_DISPLAY = pygame.display.set_mode((length, length), pygame.RESIZABLE)
    Board.GAME_DISPLAY = GAME_DISPLAY #  Sets the game display to the newly resized game display
    Board.sqr_length = math.floor(length / 8)
    Draw.draw_main_menu(GAME_DISPLAY, WIDTH, HEIGHT)


def game_loop():
    global GAME_DISPLAY
    global HEIGHT
    global WIDTH
    global CURRENT_WINDOW
    pygame.init()
    pygame.display.set_caption('My Chess')
    clock = pygame.time.Clock()
    hasQuit = False
    hasSetUpBoard = False
    hasSetUpMainMenu = False
    while not hasQuit:
        pygame.display.update()
        for event in pygame.event.get() + [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                hasQuit = True

            else:
                # Deals with input in the main menu
                if CURRENT_WINDOW == Window.MAIN_MENU:
                    if not hasSetUpMainMenu:
                        Draw.draw_main_menu(GAME_DISPLAY, WIDTH, HEIGHT)
                        hasSetUpMainMenu = True
                    elif event.type == pygame.VIDEORESIZE:
                        resize_screen(event)
                        
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                        pos = pygame.mouse.get_pos(WIDTH, HEIGHT)
                        itemSelected = MainMenu.select_menu_item(pos, WIDTH, HEIGHT)
                        if itemSelected != None:
                            CURRENT_WINDOW = itemSelected

                # Deals with input in the chess game
                elif CURRENT_WINDOW == Window.IN_GAME:
                    if not hasSetUpBoard:
                        Board.init(GAME_DISPLAY)
                        hasSetUpBoard = True
                    elif event.type == pygame.VIDEORESIZE:
                        resize_screen(event)
                    
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
                        sqr = Board.get_sqr_from_xy(pos)
                        if Board.has_chess_piece(sqr):
                            piece = Board.activePieces[sqr]
                            if piece[1] == PieceType.ROOK:
                                Board.castle(sqr)
                            elif piece[1] == PieceType.PAWN:
                                Board.promote_pawn(sqr)


                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Draw.remove_all_highlights(GAME_DISPLAY)
                            Draw.remove_selection(GAME_DISPLAY)


        clock.tick(30)


if __name__ == "__main__":
    game_loop()