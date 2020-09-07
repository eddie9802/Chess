
import socket
import sys
import threading
import pygame

import Multiplayer




def connect_to_server(host, port, gameState, condition):
    gameEnded = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.setblocking(1)
        while not gameEnded:
            with condition:
                
                # Receving a move
                Multiplayer.receive_move(gameState, s)

                #  The sending of a move
                Multiplayer.send_move(gameState, s, condition)
            


def start_connect_to_server_thread(host, port, state, condition):
    try:
        t = threading.Thread(target = connect_to_server, args=(host, port, state, condition))
        t.daemon = True # die when the main thread dies
        t.start()
    except Exception as e:
        print (e)
