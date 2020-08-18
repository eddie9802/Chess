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

LEFT_CLICK = 1
RIGHT_CLICK = 3


class GameState():
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
    setUpMainMenu = False

def _resize_screen(newScreenDimensions, gameState):
    """Takes the new size of the screen and updates the pygame display as well as the game state"""
    gameState.WIDTH = newScreenDimensions[0]
    gameState.HEIGHT = newScreenDimensions[1]
    gameState.GAME_DISPLAY = pygame.display.set_mode((gameState.WIDTH, gameState.HEIGHT), pygame.RESIZABLE)
    Board.GAME_DISPLAY = gameState.GAME_DISPLAY #  Sets the game display to the newly resized game display
    Board.sqr_length = math.floor(gameState.WIDTH / 8)

    # Redraws the appropriate screen
    if gameState.CURRENT_WINDOW == Window.TWO_PLAYER:
        Draw.redraw_board(gameState.GAME_DISPLAY)
    elif gameState.CURRENT_WINDOW == Window.MAIN_MENU:
        Draw.draw_main_menu(gameState.GAME_DISPLAY, gameState.WIDTH, gameState.HEIGHT)
    elif gameState.CURRENT_WINDOW == Window.MULTIPLAYER:
        Draw.set_up_multiplayer_screen(gameState.GAME_DISPLAY, gameState.WIDTH, gameState.HEIGHT)
    elif gameState.CURRENT_WINDOW == Window.JOIN:
        Draw.set_up_join_screen(gameState.GAME_DISPLAY, gameState.WIDTH, gameState.HEIGHT, gameState.ADDRESS, gameState.PORTSTR, gameState.JOIN_GAME_MSG)


def _main_menu_event(event, gameState):
    """Deals with an event that occurs on the main menu."""
    if not gameState.setUpMainMenu:
        # Sets up the main menu, if it is not already set up
        Draw.draw_main_menu(gameState.GAME_DISPLAY, gameState.WIDTH, gameState.HEIGHT)
        gameState.setUpMainMenu = True
    elif event.type == pygame.VIDEORESIZE:
        _resize_screen(event.size, gameState)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
        # Selects an item from the main menu
        mouseClickPos = pygame.mouse.get_pos()
        itemSelected = Menu.select_mainmenu_item(mouseClickPos, gameState.WIDTH, gameState.HEIGHT)
        if itemSelected != None:
            gameState.CURRENT_WINDOW = itemSelected
            gameState.hasSetUpMainMenu = False

def _process_left_click_ingame(mouseClickPos):
    """Takes the left mouse click position and selects a square on the chess board with it, then it checks if a checkmate has occurred"""
    moveMade = Board.select_square(mouseClickPos)
    if Board.check_for_checkmate():
        if Board.turn != Colour.WHITE:
            ptext.draw("White wins!", (20, (gameState.HEIGHT / 2) - (gameState.HEIGHT / 8)), fontsize = gameState.HEIGHT / 8, color=(255, 0, 0))
        else:
            ptext.draw("Black wins!", (20, (gameState.HEIGHT / 2) - (gameState.HEIGHT / 8)), fontsize = gameState.HEIGHT / 8, color=(255, 0, 0))
        Board.GAME_FINISHED = True

    return moveMade


def _send_left_click(mouseClickPos, gameState, condition):
    """Sends the left click pos and the selected square of the chess board, to the opponent, for them to process.
        Mouse click will not be sent, if it does not result in a move on the chess board being made."""
    prevSelectedSqr = Board.selected_sqr
    moveMade = _process_left_click_ingame(mouseClickPos)
    if moveMade == True:
        gameState.SELECTED_SQR = prevSelectedSqr
        gameState.CLICKED_POS = mouseClickPos
        gameState.MOUSE_CLICK = gameState.LEFT
        with condition:
            condition.notify()

def _process_right_click_ingame(mouseClickPos):
    """Takes the right mouse click position and checks if the user wants to castle or promote a pawn.  If they do then it executes that action.
        Returns a boolean which denotes whether a castling or pawn promotion has occurred."""
    sqr = Board.get_sqr_from_xy(mouseClickPos)
    moveMade = False
    if Board.has_chess_piece(sqr):
        piece = Board.activePieces[sqr]
        if piece[1] == PieceType.ROOK:
            moveMade = Board.castle(sqr)
        elif piece[1] == PieceType.PAWN:
            moveMade = Board.promote_pawn(sqr)
    return moveMade


def _send_right_click(mouseClickPos, condition):
    """Sends the right click position and the selected square to the oppponent only if the right click is a valid castling or pawn promotion move."""
    prevSelectedSqr = Board.selected_sqr
    moveMade = _process_right_click_ingame(mouseClickPos)
    if moveMade == True:
        gameState.CLICKED_POS = mouseClickPos
        gameState.MOUSE_CLICK = gameState.RIGHT
        gameState.SELECTED_SQR = prevSelectedSqr
        with condition:
            condition.notify()


def _receive_left_click():
    """Processes the left click and selected square that the opponent sent in multiplayer."""
    Board.selected_sqr = gameState.SELECTED_SQR
    leftClickPos = gameState.CLICKED_POS
    selectedSqrScreenPos = Board.get_sqr_xy(gameState.SELECTED_SQR)
    Board.select_square(selectedSqrScreenPos)
    Board.select_square(leftClickPos)

    # Checks if a checkmate has occurred.  If it has then the proper message is displayed to the user
    if Board.check_for_checkmate():
        if Board.turn != Colour.WHITE:
            ptext.draw("White wins!", (20, (gameState.HEIGHT / 2) - (gameState.HEIGHT / 8)), fontsize = gameState.HEIGHT / 8, color=(255, 0, 0))
        else:
            ptext.draw("Black wins!", (20, (gameState.HEIGHT / 2) - (gameState.HEIGHT / 8)), fontsize = gameState.HEIGHT / 8, color=(255, 0, 0))
        Board.GAME_FINISHED = True
    gameState.RECEIVED_MOVE = False


def _receive_right_click():
    """Processes the right click position and selected square which the opponent has sent."""
    Board.selected_sqr = gameState.SELECTED_SQR
    rightClickPos = gameState.CLICKED_POS
    _process_right_click_ingame(rightClickPos)
    gameState.RECEIVED_MOVE = False


def game_loop(gameState):
    """The main game loop of the chess program"""
    pygame.init()
    pygame.display.set_caption('My Chess')
    clock = pygame.time.Clock()
    hasQuit = False
    hasSetUpBoard = False
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
                # Deals with events on the main menu
                if gameState.CURRENT_WINDOW == Window.MAIN_MENU:
                    _main_menu_event(event, gameState)

                # Deals with input in the chess game
                elif gameState.CURRENT_WINDOW == Window.TWO_PLAYER:
                    # Sets up the initial chess board
                    if not hasSetUpBoard:
                        Board.init(gameState.GAME_DISPLAY)
                        hasSetUpBoard = True

                    # Resizes the chess board
                    elif event.type == pygame.VIDEORESIZE:
                        _resize_screen(event.size, gameState)

                    # Deals with left clicks while in game
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == gameState.LEFT:
                        mouseClickPos = pygame.mouse.get_pos()
                        if multiplayer:
                            if Board.turn == gameState.PLAYER_COLOUR:
                                _send_left_click(mouseClickPos, gameState, condition)
                        else:
                            _process_left_click_ingame(mouseClickPos)
                    
                    # Deals with right clicks while in game
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == gameState.RIGHT:
                        mouseClickPos = pygame.mouse.get_pos()
                        if multiplayer:
                            if gameState.PLAYER_COLOUR == Board.turn:
                                _send_right_click(mouseClickPos, condition)
                        else:
                            _process_right_click_ingame(mouseClickPos)

                    # Removes the selection and the highlights on the chess board
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Draw.remove_all_highlights(gameState.GAME_DISPLAY)
                            Draw.remove_selection(gameState.GAME_DISPLAY)

                    # This is for playing received moves from the opponent made with the left click
                    elif multiplayer and gameState.PLAYER_COLOUR != Board.turn and gameState.RECEIVED_MOVE and gameState.MOUSE_CLICK == gameState.LEFT:
                        _receive_left_click()

                    # This is for playing received moves from the opponent made with the right click
                    elif multiplayer and gameState.PLAYER_COLOUR != Board.turn and gameState.RECEIVED_MOVE and gameState.MOUSE_CLICK == gameState.RIGHT:
                        _receive_right_click()
                        
                
                # Draws the set up multiplayer screen
                elif gameState.CURRENT_WINDOW == Window.MULTIPLAYER_MENU:

                    # Sets up the multiplayer menu screen
                    if not hasSetUpMultiplayerMenu:
                        Draw.set_up_multiplayer_screen(gameState.GAME_DISPLAY, gameState.WIDTH, gameState.HEIGHT)
                        hasSetUpMultiplayerMenu = True

                    # Resizes the program screen
                    elif event.type == pygame.VIDEORESIZE:
                        _resize_screen(event.size, gameState)

                    # Processes left clicks in the multiplayer menu and selects the appropriate item on the menu
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == gameState.LEFT:
                        pos = pygame.mouse.get_pos()
                        itemSelected = Menu.select_multiplayermenu_item(pos, gameState.WIDTH, gameState.HEIGHT)
                        if itemSelected != None:
                            gameState.CURRENT_WINDOW = itemSelected
                            hasSetUpMultiplayerMenu = False
                
                elif gameState.CURRENT_WINDOW == Window.HOST:
                    # Sets up the host game screen.  Displays the ip address and port of the machine to the user.
                    if not hasSetUpHostMenu:
                        host, port = Server.start_server(gameState, condition)
                        Draw.set_up_host_screen(gameState, host, port)
                        hasSetUpHostMenu = True
                    else:
                        # Sets up a two player game if connection to another player has been successful
                        if gameState.CONNECTION_SUCCESS:
                            multiplayer = True
                            gameState.CURRENT_WINDOW = Window.TWO_PLAYER
                            gameState.PLAYER_COLOUR = Colour.WHITE
                            hasSetUpJoinMenu = False

                # Sets up the join game screen
                elif gameState.CURRENT_WINDOW == Window.JOIN:
                    if not hasSetUpJoinMenu:
                        Draw.set_up_join_screen(gameState.GAME_DISPLAY, gameState.WIDTH, gameState.HEIGHT, gameState.ADDRESS, gameState.PORTSTR, gameState.JOIN_GAME_MSG)
                        hasSetUpJoinMenu = True

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == gameState.LEFT:
                        pos = pygame.mouse.get_pos()
                        hasSelectedAddressBox, hasSelectedPortBox = Menu.select_join_item(pos, gameState.WIDTH, gameState.HEIGHT)
                        if itemSelected != None:
                            gameState.CURRENT_WINDOW = itemSelected
                            hasSetUpMultiplayerMenu = False

                    # Deals with key presses in the join game menu
                    elif event.type == pygame.KEYDOWN:
                        # Backspaces remove characters from the address and port
                        if event.key == pygame.K_BACKSPACE:
                            if hasSelectedAddressBox:
                                gameState.ADDRESS = gameState.ADDRESS[:-1]
                            elif hasSelectedPortBox:
                                gameState.PORTSTR = gameState.PORTSTR[:-1]
                        
                        # Return initialises a connection with the give ip address and port
                        elif event.key == pygame.K_RETURN:
                            if len(gameState.ADDRESS) > 0 and len(gameState.PORTSTR) > 0:
                                port = int(gameState.PORTSTR)
                                Client.start_connect_to_server_thread(gameState.ADDRESS, port, gameState, condition)
                                hasSetUpJoinMenu = False
                                gameState.CURRENT_WINDOW = Window.TWO_PLAYER
                                multiplayer = True
                                gameState.PLAYER_COLOUR = Colour.BLACK

                        else:
                            # Adds the inputted character to either the address box or port box
                            inputChar = chr(event.key)
                            if hasSelectedAddressBox:
                                gameState.ADDRESS = gameState.ADDRESS + inputChar
                            elif hasSelectedPortBox:
                                gameState.PORTSTR = gameState.PORTSTR + inputChar
                        Draw.set_up_join_screen(gameState.GAME_DISPLAY, gameState.WIDTH, gameState.HEIGHT, gameState.ADDRESS, gameState.PORTSTR, gameState.JOIN_GAME_MSG)

                    elif event.type == pygame.VIDEORESIZE:
                        _resize_screen(event.size, gameState)
        clock.tick(30)





if __name__ == "__main__":
    gameState = GameState()
    game_loop(gameState)