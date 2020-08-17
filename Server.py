
import socket
import miniupnpc
import atexit
import threading
import Main
import pickle
import pygame

UPNP = None
HOST = None
PORT = None


def get_free_port(host):
    port = 5001
    # testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # foundFreePort = False
    # while not foundFreePort:
    #     location = ("127.0.0.1", port)
    #     result_of_check = testSocket.connect_ex(location)

    #     if result_of_check == 0:
    #         foundFreePort = True
    #     print(port)

    #     port += 1
        
    # testSocket.close()
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


def create_server_socket(state, condition):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        state.CONNECTION_SUCCESS = True
        gameEnded = False
        with conn:
            print('Connected by', addr)
            while True:
                with condition:

                    # The sending of a move
                    condition.wait()
                    move = pickle.dumps((state.SELECTED_SQR, state.CLICKED_POS, state.MOUSE_CLICK))
                    conn.sendall(move)
                    data = conn.recv(1024)
                    move = pickle.loads(data)
                    state.SELECTED_SQR = move[0]
                    state.CLICKED_POS = move[1]
                    state.MOUSE_CLICK = move[2]
                    event = pygame.event.Event(pygame.USEREVENT)
                    event.button = state.MOUSE_CLICK
                    state.RECEIVED_MOVE = True
                    pygame.event.post(event)


def exit_handler():
    if PORT != None and HOST != None and UPNP != None:
        UPNP.deleteportmapping(PORT, 'TCP')

atexit.register(exit_handler)

def start_server(state, condition):
    global UPNP
    global HOST
    global PORT
    UPNP, HOST, PORT = forward_port()
    try:
        t = threading.Thread(target = create_server_socket, args=(state, condition, ))
        t.daemon = True # die when the main thread dies
        t.start()
    except Exception as e:
        print (e)
    return HOST, PORT

