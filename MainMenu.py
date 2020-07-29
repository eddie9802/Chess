from Window import Window

# Takes the mouse click coordinates and works out what item the user has selected on the main menu
def select_menu_item(pos, width, height):
    twoPlayerY = (height / 16) * 4
    if pos[1] >= twoPlayerY and pos[1] <= twoPlayerY + (height / 16):
        return Window.IN_GAME
    return None