
import socket
import miniupnpc
import sys
import threading
import pickle
import pygame


def connect_to_server(host, port, state, condition):
    gameEnded = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.setblocking(1)
        while not gameEnded:
            with condition:
                # The receiving of a move
                data = s.recv(1024)
                move = pickle.loads(data)
                state.SELECTED_SQR = move[0]
                state.CLICKED_POS = move[1]
                state.MOUSE_CLICK = move[2]
                print(state.MOUSE_CLICK)
                event = pygame.event.Event(pygame.USEREVENT)
                event.button = state.MOUSE_CLICK
                state.RECEIVED_MOVE = True
                pygame.event.post(event)

                #  The sending of a move
                condition.wait()
                move = pickle.dumps((state.SELECTED_SQR, state.CLICKED_POS, state.MOUSE_CLICK))
                s.sendall(move)
            

    #print('Received', repr(data))


def start_connect_to_server_thread(host, port, state, condition):
    try:
        t = threading.Thread(target = connect_to_server, args=(host, port, state, condition))
        t.daemon = True # die when the main thread dies
        t.start()
    except Exception as e:
        print (e)
