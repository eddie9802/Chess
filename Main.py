import Board
#import pkg_resources.py2_warn
import pygame
import Draw
import ptext
import Menu
import Server
import Client
import Move
from Colour import Colour
from Window import Window
from PieceType import PieceType

import math
import miniupnpc
import threading
from time import sleep


class Program_state():
    HEIGHT = 800
    WIDTH = 800
    LEFT = 1
    RIGHT = 3
    GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    CURRENT_WINDOW = Window.MAIN_MENU
    ADDRESS = ""
    PORTSTR = ""
    JOIN_GAME_MSG = ""
    PLAYER_COLOUR = None
    CONNECTION_SUCCESS = False
    SELECTED_SQR = None
    CLICKED_POS = None
    MOUSE_CLICK = None
    RECEIVED_MOVE = False

def resize_screen(event, state):

    length = min(event.size)
    state.HEIGHT = length
    state.WIDTH = length
    state.GAME_DISPLAY = pygame.display.set_mode((length, length), pygame.RESIZABLE)
    Board.GAME_DISPLAY = state.GAME_DISPLAY #  Sets the game display to the newly resized game display
    Board.sqr_length = math.floor(length / 8)
    if state.CURRENT_WINDOW == Window.MAIN_MENU:
        Draw.draw_main_menu(state.GAME_DISPLAY, state.WIDTH, state.HEIGHT)
    elif state.CURRENT_WINDOW == Window.MULTIPLAYER:
        Draw.set_up_multiplayer_screen(state.GAME_DISPLAY, state.WIDTH, state.HEIGHT)
    
    elif state.CURRENT_WINDOW == Window.JOIN:
        Draw.set_up_join_screen(state.GAME_DISPLAY, state.WIDTH, state.HEIGHT, state.ADDRESS, state.PORTSTR, state.JOIN_GAME_MSG)



def game_loop(state):
    pygame.init()
    pygame.display.set_caption('My Chess')
    clock = pygame.time.Clock()
    hasQuit = False
    hasSetUpBoard = False
    hasSetUpMainMenu = False
    hasSetUpMultiplayerMenu = False
    hasSetUpHostMenu = False
    hasSetUpJoinMenu = False
    hasSelectedAddressBox = False
    hasSelectedPortBox = False
    multiplayer = False
    lock = threading.Lock()
    condition = threading.Condition(lock)
    while not hasQuit:
        pygame.display.update()
        for event in pygame.event.get() + [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                hasQuit = True

            else:
                # Deals with input in the main menu
                if state.CURRENT_WINDOW == Window.MAIN_MENU:
                    if not hasSetUpMainMenu:
                        Draw.draw_main_menu(state.GAME_DISPLAY, state.WIDTH, state.HEIGHT)
                        hasSetUpMainMenu = True
                    elif event.type == pygame.VIDEORESIZE:
                        resize_screen(event, state)
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == state.LEFT:
                        pos = pygame.mouse.get_pos()
                        itemSelected = Menu.select_mainmenu_item(pos, state.WIDTH, state.HEIGHT)
                        if itemSelected != None:
                            state.CURRENT_WINDOW = itemSelected
                            hasSetUpMainMenu = False

                # Deals with input in the chess game
                elif state.CURRENT_WINDOW == Window.TWO_PLAYER:
                    if not hasSetUpBoard:
                        Board.init(state.GAME_DISPLAY)
                        hasSetUpBoard = True

                    elif event.type == pygame.VIDEORESIZE:
                        resize_screen(event, state)
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == state.LEFT:
                        if multiplayer:
                            if Board.turn == state.PLAYER_COLOUR:
                                pos = pygame.mouse.get_pos()
                                prevSelectedSqr = Board.selected_sqr
                                moveMade = Board.select_square(pos)
                                if Board.check_for_checkmate():
                                    if Board.turn != Colour.WHITE:
                                        ptext.draw("White wins!", (20, (state.HEIGHT / 2) - (state.HEIGHT / 8)), fontsize = state.HEIGHT / 8, color=(255, 0, 0))
                                    else:
                                        ptext.draw("Black condition = threading.Condition([lock])wins!", (20, (state.HEIGHT / 2) - (state.HEIGHT / 8)), fontsize = state.HEIGHT / 8, color=(255, 0, 0))
                                    Board.GAME_FINISHED = True
                                if moveMade == True:
                                    state.SELECTED_SQR = prevSelectedSqr
                                    state.CLICKED_POS = pos
                                    state.MOUSE_CLICK = state.LEFT
                                    print("Hello")
                                    with condition:
                                        condition.notify()
                                    print("There")

                        else:
                            pos = pygame.mouse.get_pos()
                            Board.select_square(pos)
                            if Board.check_for_checkmate():
                                if Board.turn != Colour.WHITE:
                                    ptext.draw("White wins!", (20, (state.HEIGHT / 2) - (state.HEIGHT / 8)), fontsize = state.HEIGHT / 8, color=(255, 0, 0))
                                else:
                                    ptext.draw("Black wins!", (20, (state.HEIGHT / 2) - (state.HEIGHT / 8)), fontsize = state.HEIGHT / 8, color=(255, 0, 0))
                                Board.GAME_FINISHED = True
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == state.RIGHT:
                        if multiplayer:
                            if state.PLAYER_COLOUR == Board.turn:
                                pos = pygame.mouse.get_pos()
                                prevSelectedSqr = Board.selected_sqr
                                sqr = Board.get_sqr_from_xy(pos)
                                moveMade = False
                                if Board.has_chess_piece(sqr):
                                    piece = Board.activePieces[sqr]
                                    if piece[1] == PieceType.ROOK:
                                        moveMade = Board.castle(sqr)
                                    elif piece[1] == PieceType.PAWN:
                                        moveMade = Board.promote_pawn(sqr)
                                if moveMade == True:
                                    state.CLICKED_POS = pos
                                    state.MOUSE_CLICK = state.RIGHT
                                    state.SELECTED_SQR = prevSelectedSqr
                                    with condition:
                                        condition.notify()

                        else:
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
                            Draw.remove_all_highlights(state.GAME_DISPLAY)
                            Draw.remove_selection(state.GAME_DISPLAY)

                    # This is for playing received moves from the opponent made with the left click
                    elif multiplayer and state.PLAYER_COLOUR != Board.turn and state.RECEIVED_MOVE and state.MOUSE_CLICK == state.LEFT:
                        Board.selected_sqr = state.SELECTED_SQR
                        pos = state.CLICKED_POS
                        selectedSqrScreenPos = Board.get_sqr_xy(state.SELECTED_SQR)
                        Board.select_square(selectedSqrScreenPos)
                        Board.select_square(pos)
                        if Board.check_for_checkmate():
                            if Board.turn != Colour.WHITE:
                                ptext.draw("White wins!", (20, (state.HEIGHT / 2) - (state.HEIGHT / 8)), fontsize = state.HEIGHT / 8, color=(255, 0, 0))
                            else:
                                ptext.draw("Black wins!", (20, (state.HEIGHT / 2) - (state.HEIGHT / 8)), fontsize = state.HEIGHT / 8, color=(255, 0, 0))
                            Board.GAME_FINISHED = True
                        # state.SELECTED_SQR = None
                        # state.CLICKED_POS = None
                        state.RECEIVED_MOVE = False

                    # This is for playing received moves from the opponent made with the right click
                    elif multiplayer and state.PLAYER_COLOUR != Board.turn and state.RECEIVED_MOVE and state.MOUSE_CLICK == state.RIGHT:
                        Board.selected_sqr = state.SELECTED_SQR
                        print(Board.selected_sqr)
                        pos = state.CLICKED_POS
                        sqr = Board.get_sqr_from_xy(pos)
                        if Board.has_chess_piece(sqr):
                            piece = Board.activePieces[sqr]
                            if piece[1] == PieceType.ROOK:
                                Board.castle(sqr)
                            elif piece[1] == PieceType.PAWN:
                                Board.promote_pawn(sqr)
                        state.RECEIVED_MOVE = False
                
                # Draws the set up multiplayer screen
                elif state.CURRENT_WINDOW == Window.MULTIPLAYER:
                    if not hasSetUpMultiplayerMenu:
                        Draw.set_up_multiplayer_screen(state.GAME_DISPLAY, state.WIDTH, state.HEIGHT)
                        hasSetUpMultiplayerMenu = True

                    elif event.type == pygame.VIDEORESIZE:
                        resize_screen(event, state)

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == state.LEFT:
                        pos = pygame.mouse.get_pos()
                        itemSelected = Menu.select_multiplayermenu_item(pos, state.WIDTH, state.HEIGHT)
                        if itemSelected != None:
                            state.CURRENT_WINDOW = itemSelected
                            hasSetUpMultiplayerMenu = False
                
                # Sets up the host game screen
                elif state.CURRENT_WINDOW == Window.HOST:
                    if not hasSetUpHostMenu:
                        host, port = Server.start_server(state, condition)
                        Draw.set_up_host_screen(state, host, port)
                        hasSetUpHostMenu = True
                    else:
                        if state.CONNECTION_SUCCESS:
                            multiplayer = True
                            state.CURRENT_WINDOW = Window.TWO_PLAYER
                            state.PLAYER_COLOUR = Colour.WHITE
                            hasSetUpJoinMenu = False

                # Sets up the join game screen
                elif state.CURRENT_WINDOW == Window.JOIN:
                    if not hasSetUpJoinMenu:
                        Draw.set_up_join_screen(state.GAME_DISPLAY, state.WIDTH, state.HEIGHT, state.ADDRESS, state.PORTSTR, state.JOIN_GAME_MSG)
                        hasSetUpJoinMenu = True

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == state.LEFT:
                        pos = pygame.mouse.get_pos()
                        hasSelectedAddressBox, hasSelectedPortBox = Menu.select_join_item(pos, state.WIDTH, state.HEIGHT)
                        if itemSelected != None:
                            state.CURRENT_WINDOW = itemSelected
                            hasSetUpMultiplayerMenu = False

                    # Deals with key presses
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            if hasSelectedAddressBox:
                                state.ADDRESS = state.ADDRESS[:-1]
                            elif hasSelectedPortBox:
                                state.PORTSTR = state.PORTSTR[:-1]
                        elif event.key == pygame.K_RETURN:
                            if len(state.ADDRESS) > 0 and len(state.PORTSTR) > 0:
                                port = int(state.PORTSTR)
                                Client.start_connect_to_server_thread(state.ADDRESS, port, state, condition)
                                hasSetUpJoinMenu = False
                                state.CURRENT_WINDOW = Window.TWO_PLAYER
                                multiplayer = True
                                state.PLAYER_COLOUR = Colour.BLACK

                        else:
                            inputChar = chr(event.key)
                            if hasSelectedAddressBox:
                                state.ADDRESS = state.ADDRESS + inputChar
                            elif hasSelectedPortBox:
                                state.PORTSTR = state.PORTSTR + inputChar
                        Draw.set_up_join_screen(state.GAME_DISPLAY, state.WIDTH, state.HEIGHT, state.ADDRESS, state.PORTSTR, state.JOIN_GAME_MSG)

                    elif event.type == pygame.VIDEORESIZE:
                        resize_screen(event, state)
        clock.tick(30)





if __name__ == "__main__":
    state = Program_state()
    game_loop(state)