
import socket
import atexit
import threading
import subprocess
import os

import Multiplayer
import Main

INTERNALIP = None
PORT = None
EXTERNALIP = None


def get_free_port(host):
    port = 5001
    foundFreePort = False
    while not foundFreePort:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                foundFreePort = True
        except Exception as e:
            port += 1
            print(e)
    return port


def forward_port():

    # Gets the internal and external ip addresses of the device
    os.system('ip route get 8.8.8.8 | sed -n \'/src/{s/.*src *\\([^ ]*\\).*/\\1/p;q}\' > tmp')
    os.system('curl ifconfig.me >> tmp')
    with open("tmp") as f:
        interalIP = f.readline().rstrip('\n')
        externalIP = f.readline().rstrip('\n')
    os.system('rm tmp')

    port = get_free_port(interalIP)
    os.system('upnpc -a ' + interalIP + ' ' + str(port) + ' ' + str(port) + ' tcp')

    return interalIP, port, externalIP



def create_server_socket(gameState, condition):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((INTERNALIP, PORT))
        s.listen()
        conn, addr = s.accept()
        gameState.CONNECTION_SUCCESS = True
        gameEnded = False
        with conn:
            print('Connected by', addr)
            while True:
                with condition:
                    #  The sending of a move
                    Multiplayer.send_move(gameState, conn, condition)

                    # Receving a move
                    Multiplayer.receive_move(gameState, conn)



def exit_handler():
    if PORT != None and EXTERNALIP != None and INTERNALIP != None:
        os.system('upnpc -d ' + str(PORT) + ' tcp')

atexit.register(exit_handler)

def start_server(gameState, condition):
    global INTERNALIP
    global PORT
    global EXTERNALIP
    INTERNALIP, PORT, EXTERNALIP = forward_port()
    try:
        t = threading.Thread(target = create_server_socket, args=(gameState, condition, ))
        t.daemon = True # die when the main thread dies
        t.start()
    except Exception as e:
        print (e)
    return EXTERNALIP, PORT

