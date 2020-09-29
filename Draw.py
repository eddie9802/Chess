import pygame
import math
import ptext

import Board
from PieceType import PieceType
from Colour import Colour


BEIGE = pygame.Color(245,245,220)
GRAY = pygame.Color(128,128,128)
WHITE = BEIGE
BLACK = GRAY
HIGHLIGHTED_BEIGE = pygame.Color(245,245,170)
HIGHLIGHTED_GRAY = pygame.Color(128, 128, 78)
HIGHLIGHTED_WHITE = HIGHLIGHTED_BEIGE
HIGHLIGHTED_BLACK = HIGHLIGHTED_GRAY


def remove_selection_outline(gameDisplay):
    """Removes the selection outline from the current selected square"""
    selected_sqr = Board.selected_sqr
    if Board.PLAYER_COLOUR == Colour.BLACK and Board.selected_sqr != None:
        invertedSqr = invertSqr(Board.selected_sqr)
        selected_sqr = invertedSqr
    if selected_sqr != None:
        x = ord(selected_sqr[0]) - 97
        y = 8 - selected_sqr[1]
        colour = Board.get_square_colour(selected_sqr)
        rect = pygame.Rect(x * Board.sqr_length, y * Board.sqr_length, Board.sqr_length, Board.sqr_length)
        pygame.draw.rect(gameDisplay, colour, rect)


        piece_path = "./Data/Images/pieces/01_classic/" + Board.activePieces[Board.selected_sqr][2] + ".png"
        image = pygame.transform.scale(pygame.image.load(piece_path), (Board.sqr_length, Board.sqr_length))
        gameDisplay.blit(image, (x * Board.sqr_length, y * Board.sqr_length))





# Draws a square around the selected square of the chess board
def draw_selection(gameDisplay, square):

    sqr = square
    if Board.PLAYER_COLOUR == Colour.BLACK:
        invertedSqr = invertSqr(square)
        square = invertedSqr

    x = ord(square[0]) - 97
    y = 8 - square[1]

    # Removes the selection from the previously selected square
    remove_selection_outline(gameDisplay)

    # Draws a border around a square by drawing two overlapping squares
    rect1 = pygame.Rect(x * Board.sqr_length, y * Board.sqr_length, Board.sqr_length, Board.sqr_length)
    aqua_blue = pygame.Color(40, 113, 134)
    pygame.draw.rect(gameDisplay, aqua_blue, rect1)


    tenth = math.floor(Board.sqr_length / 10)
    twentieth = math.floor(Board.sqr_length / 20)
    rect2 = pygame.Rect(x * Board.sqr_length + twentieth, y * Board.sqr_length + twentieth, Board.sqr_length - tenth, Board.sqr_length - tenth)
    rect2_colour = Board.get_square_colour(square)
    pygame.draw.rect(gameDisplay, rect2_colour, rect2)

    piece_path = "./Data/Images/pieces/01_classic/" + Board.activePieces[sqr][2] + ".png"
    image = pygame.transform.scale(pygame.image.load(piece_path), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (x * Board.sqr_length, y * Board.sqr_length))


# Draws piece at square
def draw_piece(gameDisplay, piece, square):
    if Board.PLAYER_COLOUR == Colour.BLACK:
        invertedSqr = invertSqr(square)
        square = invertedSqr
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/" + piece[2] + ".png"), (Board.sqr_length, Board.sqr_length))
    x = ord(square[0]) - 97 # Gets the x axis value of the piece

    y = 8 - square[1]
    gameDisplay.blit(image, (x * Board.sqr_length, y * Board.sqr_length))


# Draws an empty square at the position square
def draw_empty_square(gameDisplay, square, colour):
    if Board.PLAYER_COLOUR == Colour.BLACK:
        invertedSqr = invertSqr(square)
        square = invertedSqr
    x = ord(square[0]) - 97
    y = 8 - square[1]

    rect = pygame.Rect(x * Board.sqr_length, y * Board.sqr_length, Board.sqr_length, Board.sqr_length)
    pygame.draw.rect(gameDisplay, colour, rect)


def draw_empty_board(gameDisplay):
    """Draws an empty board"""
    isBeige = False
    for x in range(8):
        isBeige = not isBeige
        for y in range(8):
            colour = None
            if isBeige:
                colour = BEIGE # Colours the square beige
            else:
                colour = GRAY # Colours the square gray
            rect = pygame.Rect(x * Board.sqr_length, y * Board.sqr_length, Board.sqr_length, Board.sqr_length)
            pygame.draw.rect(gameDisplay, colour, rect)
            isBeige = not isBeige


# Takes a square and applies a highlight to it
def highlight_square(gameDisplay, sqr):
    highlight_colour = None
    if Board.get_square_colour(sqr) == WHITE:
        highlight_colour = HIGHLIGHTED_WHITE
    else:
        highlight_colour = HIGHLIGHTED_BLACK
    draw_empty_square(gameDisplay, sqr, highlight_colour)
    if Board.has_chess_piece(sqr):
        piece = Board.activePieces[sqr]
        draw_piece(gameDisplay, piece, sqr)
    Board.highlightsOn = True


# Removes the highlight from sqr
def remove_highlight(gameDisplay, sqr):
    colour = Board.get_square_colour(sqr)
    draw_empty_square(gameDisplay, sqr, colour)
    if Board.has_chess_piece(sqr):
        piece = Board.activePieces[sqr]
        draw_piece(gameDisplay, piece, sqr)


# Removes all the highlights that are current on the board
def remove_all_highlights(gameDisplay):
    highlighted_sqrs = Board.get_highlighted_sqrs()
    for sqr in highlighted_sqrs:
        remove_highlight(gameDisplay, sqr)
    Board.highlightsOn = False



# Fills the chess board
def populate_board(gameDisplay):

    length = Board.sqr_length
    # Draws all black pieces

    # Draws Black rooks
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/b-rook.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (0,0))
    gameDisplay.blit(image, (length * 7, 0))

    # Draws black knights
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/b-knight.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (Board.sqr_length,0))
    gameDisplay.blit(image, (length * 6, 0))

    # Draws black bishops
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/b-bishop.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 2,0))
    gameDisplay.blit(image, (length * 5, 0))

    # Draws black queen
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/b-queen.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 3,0))

    # Draws black king
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/b-king.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 4,0))

    # Draws black pawn
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/b-pawn.png"), (Board.sqr_length, Board.sqr_length))
    for x in range(8):
        gameDisplay.blit(image, (x * Board.sqr_length,Board.sqr_length))

    
    # Draws all white pieces

    # Draws white rooks
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/w-rook.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (0, length * 7))
    gameDisplay.blit(image, (length * 7, length * 7))

    # Draws white knights
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/w-knight.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (Board.sqr_length, length * 7))
    gameDisplay.blit(image, (length * 6, length * 7))

    # Draws white bishops
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/w-bishop.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 2, length * 7))
    gameDisplay.blit(image, (length * 5, length * 7))

    # Draws white queen
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/w-queen.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 3, length * 7))

    # Draws white king
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/w-king.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 4, length * 7))

    # Draws white pawn
    image = pygame.transform.scale(pygame.image.load("./Data/Images/pieces/01_classic/w-pawn.png"), (Board.sqr_length, Board.sqr_length))
    for x in range(8):
        gameDisplay.blit(image, (x * length, length * 6))


# Draws the promotion menu on pawn's square when its at the end of its run and the user has right clicked on it
def draw_promotion_menu(gameDisplay, sqr):
    green = pygame.Color(124,252,0)
    draw_empty_square(gameDisplay, sqr, green)

    x = (ord(sqr[0]) - 97) * Board.sqr_length
    y = (8 - sqr[1]) * Board.sqr_length

    sqr_length_fifth = Board.sqr_length / 5
    
    ptext.draw("Rook", (x, y), fontsize = sqr_length_fifth*1.8, color=(0,0,0))
    ptext.draw("Knight", (x, y + (sqr_length_fifth)), fontsize = sqr_length_fifth*1.8, color=(0,0,0))
    ptext.draw("Bishop", (x, y + (sqr_length_fifth * 2)), fontsize = sqr_length_fifth*1.8, color=(0,0,0))
    ptext.draw("Queen", (x, y + (sqr_length_fifth * 3)), fontsize = sqr_length_fifth*1.8, color=(0,0,0))
    ptext.draw("Cancel", (x, y + (sqr_length_fifth * 4)), fontsize = sqr_length_fifth*1.8, color=(0,0,0))



# Removes any promotion menus that are currently present on the board
def remove_promotion_menus(gameDisplay):
    for sqr in Board.promotion_menu_sqrs:
        sqrColour = Board.get_square_colour(sqr)
        draw_empty_square(gameDisplay, sqr, sqrColour)
        piece = Board.activePieces[sqr]
        draw_piece(gameDisplay, piece, sqr)
    Board.promotion_menu_sqrs = []


def highlight_all_squares(gameDisplay):
    highlighted_sqrs = Board.get_highlighted_sqrs()
    for sqr in highlighted_sqrs:
        highlight_square(gameDisplay, sqr)

def invertSqr(sqr):
    """Takes a square and inverts its rank and file to get the inverted sqr of that square."""
    rank = sqr[0]
    rankNum = ord(rank) - 97
    invertedRankNum = 7 - rankNum
    invertedRank = chr(invertedRankNum + 97)

    sqrFile = sqr[1]
    invertedSqrFile = 9 - sqrFile

    invertedSqr = (invertedRank, invertedSqrFile)
    return invertedSqr

def redraw_board(gameDisplay):
    draw_empty_board(gameDisplay)
    for sqr in Board.activePieces:
        piece = Board.activePieces[sqr]
        colour = Board.get_square_colour(sqr)
        draw_empty_square(gameDisplay, sqr, colour)
        draw_piece(gameDisplay, piece, sqr)
    
    selSqr = Board.selected_sqr
    highlight_all_squares(gameDisplay)

    if Board.selected_sqr != None:
        draw_selection(gameDisplay, Board.selected_sqr)
    Board.selected_sqr = selSqr

    for sqr in Board.promotion_menu_sqrs:
        draw_promotion_menu(gameDisplay, sqr)

    boardLength = Board.sqr_length * 8

    if Board.GAME_FINISHED:
        if Board.turn != Colour.WHITE:
            ptext.draw("White wins!", (Board.sqr_length / 5, (boardLength / 2) - (boardLength / 8)), fontsize = boardLength / 8, color=(255, 0, 0))
        else:
            ptext.draw("Black wins!", (Board.sqr_length / 5, (boardLength / 2) - (boardLength / 8)), fontsize = boardLength / 8, color=(255, 0, 0))


def draw_main_menu(gameDisplay, width, height):
    # Draws the main menu background
    background = pygame.Rect(0, 0, width, height)
    backgroundColour = pygame.Color(252, 219, 126)
    pygame.draw.rect(gameDisplay, backgroundColour, background)

    fontsize = min(width, height) / 8
    titleX = width / 80
    titleY = height / 16

    # Draws the title
    ptext.draw("Chess", (titleX, titleY), color=(255, 0, 0), fontsize = fontsize, underline=True)


    itemFontSize = fontsize * 2/3

    # Draws the items of the main menu
    ptext.draw("2 player", (titleX, titleY * 4), color = (255, 0, 0), fontsize = itemFontSize)
    ptext.draw("Multiplayer", (titleX, titleY * 5), color = (255, 0, 0), fontsize = itemFontSize)


def set_up_multiplayer_screen(gameDisplay, width, height):
    # Draws the background of the set up multiplayer screen
    background = pygame.Rect(0, 0, width, height)
    backgroundColour = pygame.Color(252, 219, 126)
    pygame.draw.rect(gameDisplay, backgroundColour, background)

    fontsize = min(width, height) / 8
    titleX = width / 80
    titleY = height / 16

    # Draws the title
    ptext.draw("Set up game", (titleX, titleY), color=(255, 0, 0), fontsize = fontsize, underline=True)

    itemFontSize = fontsize * 2/3

    # Draws the items of the multiplayer menu
    ptext.draw("Host game", (titleX, titleY * 4), color = (255, 0, 0), fontsize = itemFontSize)
    ptext.draw("Join game", (titleX, titleY * 5), color = (255, 0, 0), fontsize = itemFontSize)


def set_up_host_screen(state, host, port):
    # Draws the background of the set up multiplayer screen
    background = pygame.Rect(0, 0, state.WIDTH, state.HEIGHT)
    backgroundColour = pygame.Color(252, 219, 126)
    pygame.draw.rect(state.GAME_DISPLAY, backgroundColour, background)

    fontsize = min(state.WIDTH, state.HEIGHT) / 8
    titleX = state.WIDTH / 80
    titleY = state.HEIGHT / 16

    # Draws the title
    ptext.draw("Host game", (titleX, titleY), color=(255, 0, 0), fontsize = fontsize, underline=True)

    itemFontSize = fontsize * 2/3

    # Draws the items of the multiplayer menu
    ptext.draw("IP Address: " + host, (titleX, titleY * 4), color = (255, 0, 0), fontsize = itemFontSize)
    ptext.draw("Port: " + str(port), (titleX, titleY * 5), color = (255, 0, 0), fontsize = itemFontSize)


def set_up_join_screen(gameDisplay, width, height, address, portStr, joinGameMsg):
    # Draws the background of the set up multiplayer screen
    background = pygame.Rect(0, 0, width, height)
    backgroundColour = pygame.Color(252, 219, 126)
    pygame.draw.rect(gameDisplay, backgroundColour, background)

    fontsize = min(width, height) / 8
    titleX = width / 80
    titleY = height / 16

    # Draws the title
    ptext.draw("Join game", (titleX, titleY), color=(255, 0, 0), fontsize = fontsize, underline=True)

    itemFontSize = fontsize * 1/2

    # Draws the input box of the ip address
    ipBoxBlack = pygame.Rect(width/3, titleY * 7, width * 2/3, itemFontSize)
    black = pygame.Color(0, 0, 0)
    pygame.draw.rect(gameDisplay, black, ipBoxBlack)

    ipBoxWhite = pygame.Rect(width/3 + 2, titleY * 7 + 2, width * 2/3 - 4, itemFontSize - 4)
    white = pygame.Color(255, 255, 255)
    pygame.draw.rect(gameDisplay, white, ipBoxWhite)

    ptext.draw(address, (ipBoxBlack.x, ipBoxBlack.y), color = (255, 0, 0), fontsize = itemFontSize - 4)

    # Draws the input box of the port
    portBoxBlack = pygame.Rect(width/3, titleY * 8, width * 2/3, itemFontSize)
    black = pygame.Color(0, 0, 0)
    pygame.draw.rect(gameDisplay, black, portBoxBlack)

    portBoxWhite = pygame.Rect(width/3 + 2, titleY * 8 + 2, width * 2/3 - 4, itemFontSize - 4)
    white = pygame.Color(255, 255, 255)
    pygame.draw.rect(gameDisplay, white, portBoxWhite)

    ptext.draw(portStr, (portBoxWhite.x, portBoxWhite.y), color = (255, 0, 0), fontsize = itemFontSize - 4)

    # Draws the items of the multiplayer menu
    ptext.draw("Please enter the IP address and the port", (titleX, titleY * 4), color = (255, 0, 0), fontsize = itemFontSize)
    ptext.draw("of the host you want to join.", (titleX, titleY * 5), color = (255, 0, 0), fontsize = itemFontSize)
    ptext.draw("IP Address: ", (titleX, titleY * 7), color = (255, 0, 0), fontsize = itemFontSize)
    ptext.draw("Port: ", (titleX, titleY * 8), color = (255, 0, 0), fontsize = itemFontSize)


    ptext.draw(joinGameMsg, (titleX, titleY * 10), color = (255, 0, 0), fontsize = itemFontSize)









