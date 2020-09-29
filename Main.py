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
    typeOfMove = None
    sentPiece = None

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
    retVal = _process_left_click_ingame(mouseClickPos)
    # Inverts the mouse click if the black player has made a move so that the correct piece is selected on the white players side
    if gameState.PLAYER_COLOUR == Colour.BLACK and Board.turn != Colour.BLACK:
        mouseClickPos = _invert_mouse_click(mouseClickPos)
    if retVal == "MoveMade":
        gameState.SELECTED_SQR = prevSelectedSqr
        gameState.CLICKED_POS = mouseClickPos
        gameState.MOUSE_CLICK = gameState.LEFT
        gameState.typeOfMove = retVal
        with condition:
            condition.notify()
    elif retVal == "PawnPromoted":
        gameState.SELECTED_SQR = prevSelectedSqr
        gameState.CLICKED_POS = mouseClickPos
        gameState.MOUSE_CLICK = gameState.LEFT
        gameState.typeOfMove = retVal
        gameState.sentPiece = Board.activePieces[prevSelectedSqr]
        with condition:
            condition.notify()


def _process_right_click_ingame(mouseClickPos):
    """Takes the right mouse click position and checks if the user wants to castle or promote a pawn.  If they do then it executes that action.
        Returns a boolean which denotes whether a castling or pawn promotion has occurred."""
    selectedSqr = None
    sqr = Board.get_sqr_from_xy(mouseClickPos)
    retVal = "NoMoveMade"
    if gameState.PLAYER_COLOUR == Colour.BLACK and Board.turn == Colour.BLACK:
        mouseClickPos = _invert_mouse_click(mouseClickPos)
    if Board.has_chess_piece(sqr):
        piece = Board.activePieces[sqr]
        if piece[1] == PieceType.ROOK:
            selectedSqr = Board.selected_sqr
            retVal = Board.castle(sqr)
        elif piece[1] == PieceType.PAWN:
            selectedSqr = sqr
            Board.selected_sqr = selectedSqr
            Board.promote_pawn(sqr)
    return retVal, selectedSqr


def _send_right_click(mouseClickPos, condition, gameState):
    """Sends the right click position and the selected square to the oppponent only if the right click is a valid castling or pawn promotion move."""
    retVal, prevSelectedSqr = _process_right_click_ingame(mouseClickPos)

    if gameState.PLAYER_COLOUR == Colour.BLACK and Board.turn == Colour.BLACK:
        mouseClickPos = _invert_mouse_click(mouseClickPos)

    if retVal == "MoveMade":
        gameState.SELECTED_SQR = prevSelectedSqr
        gameState.CLICKED_POS = mouseClickPos
        gameState.MOUSE_CLICK = gameState.LEFT
        gameState.typeOfMove = retVal
        with condition:
            condition.notify()


def _receive_left_click(gameState):
    """Processes the left click and selected square that the opponent sent in multiplayer."""
    if gameState.typeOfMove == "MoveMade":
        Board.selected_sqr = gameState.SELECTED_SQR
        selectedSqrScreenPos = Board.get_sqr_xy(gameState.SELECTED_SQR)
        Board.select_square(selectedSqrScreenPos)
        leftClickPos = gameState.CLICKED_POS
        Board.select_square(leftClickPos)
    elif gameState.typeOfMove == "PawnPromoted":
        Board.activePieces[gameState.SELECTED_SQR] = gameState.sentPiece
        colour = Board.get_square_colour(gameState.SELECTED_SQR)
        Draw.draw_empty_square(gameState.GAME_DISPLAY, gameState.SELECTED_SQR, colour)
        Draw.draw_piece(gameState.GAME_DISPLAY, gameState.sentPiece, gameState.SELECTED_SQR)
        if Board.turn == Colour.WHITE:
            Board.turn = Colour.BLACK
        else:
            Board.turn = Colour.WHITE

    # Checks if a checkmate has occurred.  If it has then the proper message is displayed to the user
    if Board.check_for_checkmate():
        if Board.turn != Colour.WHITE:
            ptext.draw("White wins!", (20, (gameState.HEIGHT / 2) - (gameState.HEIGHT / 8)), fontsize = gameState.HEIGHT / 8, color=(255, 0, 0))
        else:
            ptext.draw("Black wins!", (20, (gameState.HEIGHT / 2) - (gameState.HEIGHT / 8)), fontsize = gameState.HEIGHT / 8, color=(255, 0, 0))
        Board.GAME_FINISHED = True
    gameState.RECEIVED_MOVE = False
        


def _receive_right_click(gameState):
    """Processes the right click position and selected square which the opponent has sent."""
    Board.selected_sqr = gameState.SELECTED_SQR
    rightClickPos = gameState.CLICKED_POS
    _process_right_click_ingame(rightClickPos)
    gameState.RECEIVED_MOVE = False


def _invert_mouse_click(mouseClickPos):
    """Takes the position that the mouse click occurred and inverts it."""
    invertedX = (Board.sqr_length * 8) - mouseClickPos[0]
    invertedY = (Board.sqr_length * 8) - mouseClickPos[1]
    invertedMouseClick = (invertedX, invertedY)
    return invertedMouseClick


def game_loop(gameState):
    """The main game loop of the chess program"""

    pygame.init()
    pygame.display.set_caption('Chess Master')
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
                        Board.init(gameState.GAME_DISPLAY, gameState.PLAYER_COLOUR)
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
                                _send_right_click(mouseClickPos, condition, gameState)
                        else:
                            _process_right_click_ingame(mouseClickPos)

                    # Removes the selection and the highlights on the chess board
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Draw.remove_all_highlights(gameState.GAME_DISPLAY)
                            Draw.remove_selection_outline(gameState.GAME_DISPLAY)

                    # This is for playing received moves from the opponent made with the left click
                    elif multiplayer and gameState.PLAYER_COLOUR != Board.turn and gameState.RECEIVED_MOVE and gameState.MOUSE_CLICK == gameState.LEFT:
                        _receive_left_click(gameState)

                    # This is for playing received moves from the opponent made with the right click
                    elif multiplayer and gameState.PLAYER_COLOUR != Board.turn and gameState.RECEIVED_MOVE and gameState.MOUSE_CLICK == gameState.RIGHT:
                        _receive_right_click(gameState)
                        
                
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