
import socket
import miniupnpc
import atexit
import threading

import Multiplayer
import Main

UPNP = None
HOST = None
PORT = None


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
    upnp = miniupnpc.UPnP()

    upnp.discoverdelay = 10
    upnp.discover()

    upnp.selectigd()
    port = get_free_port(upnp.lanaddr)
    # r = upnp.getspecificportmapping(port, 'TCP')
    # while r != None and port < 65536:
    #     port += 1
    r = upnp.getspecificportmapping(port, 'TCP')

    # addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
    upnp.addportmapping(port, 'TCP', upnp.lanaddr, port, 'testing', '')
    return upnp, upnp.lanaddr, port 



def create_server_socket(gameState, condition):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
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
    if PORT != None and HOST != None and UPNP != None:
        UPNP.deleteportmapping(PORT, 'TCP')

atexit.register(exit_handler)

def start_server(gameState, condition):
    global UPNP
    global HOST
    global PORT
    UPNP, HOST, PORT = forward_port()
    try:
        t = threading.Thread(target = create_server_socket, args=(gameState, condition, ))
        t.daemon = True # die when the main thread dies
        t.start()
    except Exception as e:
        print (e)
    return HOST, PORT

