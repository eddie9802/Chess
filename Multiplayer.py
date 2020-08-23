import pickle
import pygame

import Board
import Move
from Colour import Colour


def receive_move(gameState, socket):
    """Receives a move from the opponent and sets the game state using the selected sqr, mouse click position and the type of mouse click that was sent."""
    data = socket.recv(1024)
    msg = pickle.loads(data)
    gameState.typeOfMove = msg[0]
    gameState.SELECTED_SQR = msg[1]
    gameState.CLICKED_POS = msg[2]
    gameState.MOUSE_CLICK = msg[3]
    if gameState.typeOfMove == "PawnPromoted":
        gameState.sentPiece = msg[4]
    event = pygame.event.Event(pygame.USEREVENT)
    event.button = gameState.MOUSE_CLICK
    gameState.RECEIVED_MOVE = True
    pygame.event.post(event)


def send_move(gameState, socket, condition):
    """Sends a move to the opponent which is the selected sqr, the mouse click position and the type of mouse click."""
    condition.wait()
    msg = None
    if gameState.typeOfMove == "MoveMade":
        msg = (gameState.typeOfMove, gameState.SELECTED_SQR, gameState.CLICKED_POS, gameState.MOUSE_CLICK)
    elif gameState.typeOfMove == "PawnPromoted":
        msg = (gameState.typeOfMove, gameState.SELECTED_SQR, gameState.CLICKED_POS, gameState.MOUSE_CLICK, gameState.sentPiece)
    pickledMsg = pickle.dumps(msg)
    socket.sendall(pickledMsg)
