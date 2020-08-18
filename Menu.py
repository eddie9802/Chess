from Window import Window

# Takes the mouse click coordinates and works out what item the user has selected on the main menu
def select_mainmenu_item(pos, width, height):
    twoPlayerY = (height / 16) * 4
    if pos[1] >= twoPlayerY and pos[1] <= twoPlayerY + (height / 16):
        return Window.TWO_PLAYER

    multiplayerY = (height / 16) * 5
    if pos[1] >= multiplayerY and pos[1] <= multiplayerY + (height / 16):
        return Window.MULTIPLAYER_MENU
    return None

# Takes the mouse click coordinates and works out what item the user has selected on the main menu
def select_multiplayermenu_item(pos, width, height):
    hostGameY = (height / 16) * 4
    if pos[1] >= hostGameY and pos[1] <= hostGameY + (height / 16):
        return Window.HOST

    joinGameY = (height / 16) * 5
    if pos[1] >= joinGameY and pos[1] <= joinGameY + (height / 16):
        return Window.JOIN
    return None


def select_join_item(pos, width, height):
    ipBoxSelected = False
    portBoxSelected = False
    ipBoxX = width/3 + 2
    ipBoxY = height / 16 * 7 + 2

    portBoxX = width/3 + 2
    portBoxY = height / 16 * 8 + 2

    boxWidth = width * 2/3
    boxHeight = min(width, height) / 16

    if pos[0] >= ipBoxX and pos[0] <= ipBoxX + boxWidth and pos[1] >= ipBoxY and pos[1] <= ipBoxY + boxHeight:
        ipBoxSelected = True
    elif pos[0] >= portBoxX and pos[0] <= portBoxX + boxWidth and pos[1] >= portBoxY and pos[1] <= portBoxY + boxHeight:
        portBoxSelected = True

    return ipBoxSelected, portBoxSelected

