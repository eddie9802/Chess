import pygame
import math

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


# Removes the selection from the selected square
def remove_selection(gameDisplay):
    selectedSquare = Board.selectedSquare
    if selectedSquare != None:
        x = ord(selectedSquare[0]) - 97
        y = 8 - selectedSquare[1]
        colour = Board.get_square_colour(selectedSquare)
        rect = pygame.Rect(x * 100, y * 100, 100, 100)
        pygame.draw.rect(gameDisplay, colour, rect)


        piece_path = "./Images/pieces/01_classic/" + Board.activePieces[selectedSquare][2] + ".png"
        image = pygame.transform.scale(pygame.image.load(piece_path), (100, 100))
        gameDisplay.blit(image, (x * 100, y * 100))

        Board.selectedSquare = None




# Draws a square around the selected square of the chess board
def draw_selection(gameDisplay, square):
    x = ord(square[0]) - 97
    y = 8 - square[1]

    # Removes the selection from the previously selected square
    remove_selection(gameDisplay)

    # Draws a border around a square by drawing two overlapping squares
    rect1 = pygame.Rect(x * 100, y * 100, 100, 100)
    aqua_blue = pygame.Color(40, 113, 134)
    pygame.draw.rect(gameDisplay, aqua_blue, rect1)

    rect2 = pygame.Rect(x * 100 + 5, y * 100 + 5, 90, 90)
    rect2_colour = Board.get_square_colour(square)
    pygame.draw.rect(gameDisplay, rect2_colour, rect2)

    piece_path = "./Images/pieces/01_classic/" + Board.activePieces[square][2] + ".png"
    image = pygame.transform.scale(pygame.image.load(piece_path), (100, 100))
    gameDisplay.blit(image, (x * 100, y * 100))


# Draws piece at square
def draw_piece(gameDisplay, piece, square):
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/" + piece[2] + ".png"), (100, 100))
    x = ord(square[0]) - 97 # Gets the x axis value of the piece

    y = 8 - square[1]
    gameDisplay.blit(image, (x * 100, y * 100))


# Draws an empty square at the position square
def draw_empty_square(gameDisplay, square, colour):
    x = ord(square[0]) - 97
    y = 8 - square[1]

    rect = pygame.Rect(x * 100, y * 100, 100, 100)
    pygame.draw.rect(gameDisplay, colour, rect)


# Draws an empty board
def draw_empty_board(gameDisplay):
    isBeige = False
    # Colours squares based on the parity of their rank and file
    for x in range(8):
        isBeige = not isBeige
        for y in range(8):
            colour = None
            if isBeige:
                colour = BEIGE # Colours the square beige
            else:
                colour = GRAY # Colours the square gray
            rect = pygame.Rect(x * 100, y * 100, 100, 100)
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


def remove_highlight(gameDisplay, sqr):
    colour = Board.get_square_colour(sqr)
    draw_empty_square(gameDisplay, sqr, colour)
    if Board.has_chess_piece(sqr):
        piece = Board.activePieces[sqr]
        draw_piece(gameDisplay, piece, sqr)


def remove_all_highlights(gameDisplay, highlighted_squares):
    for sqr in highlighted_squares:
        remove_highlight(gameDisplay, sqr)
    Board.highlightsOn = False



# Fills the chess board
def populate_board(gameDisplay):

    # Draws all black pieces

    # Draws Black rooks
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-rook.png"), (100, 100))
    gameDisplay.blit(image, (0,0))
    gameDisplay.blit(image, (700, 0))

    # Draws black knights
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-knight.png"), (100, 100))
    gameDisplay.blit(image, (100,0))
    gameDisplay.blit(image, (600, 0))

    # Draws black bishops
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-bishop.png"), (100, 100))
    gameDisplay.blit(image, (200,0))
    gameDisplay.blit(image, (500, 0))

    # Draws black queen
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-queen.png"), (100, 100))
    gameDisplay.blit(image, (300,0))

    # Draws black king
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-king.png"), (100, 100))
    gameDisplay.blit(image, (400,0))

    # Draws black pawn
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-pawn.png"), (100, 100))
    for x in range(8):
        gameDisplay.blit(image, (x * 100,100))

    
    # Draws all white pieces

    # Draws white rooks
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-rook.png"), (100, 100))
    gameDisplay.blit(image, (0, 700))
    gameDisplay.blit(image, (700, 700))

    # Draws white knights
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-knight.png"), (100, 100))
    gameDisplay.blit(image, (100,700))
    gameDisplay.blit(image, (600, 700))

    # Draws white bishops
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-bishop.png"), (100, 100))
    gameDisplay.blit(image, (200, 700))
    gameDisplay.blit(image, (500, 700))

    # Draws white queen
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-queen.png"), (100, 100))
    gameDisplay.blit(image, (300, 700))

    # Draws white king
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-king.png"), (100, 100))
    gameDisplay.blit(image, (400, 700))

    # Draws white pawn
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-pawn.png"), (100, 100))
    for x in range(8):
        gameDisplay.blit(image, (x * 100, 600))


def draw_promotion_menu(gameDisplay, sqr):
    green = pygame.Color(124,252,0)
    draw_empty_square(gameDisplay, sqr, green)

    x = (ord(sqr[0]) - 97) * 100
    y = (8 - sqr[1]) * 100
    
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    rook = myfont.render('Rook', True, (0, 0, 0))
    knight = myfont.render('Knight', True, (0, 0, 0))
    bishop = myfont.render('Bishop', True, (0, 0, 0))
    queen = myfont.render('Queen', True, (0, 0, 0))
    cancel = myfont.render('Cancel', True, (0, 0, 0))

    gameDisplay.blit(rook,(x,y))
    gameDisplay.blit(knight,(x, y + 20))
    gameDisplay.blit(bishop,(x, y + 40))
    gameDisplay.blit(queen,(x, y + 60))
    gameDisplay.blit(cancel,(x, y + 80))

    Board.promotion_menu_sqrs.append(sqr)


def draw_menu_selection(gameDisplay, sqr, pos):
    y = (8 - sqr[1]) * 100
    offset = pos[1] - y
    num = math.floor(offset / 20)
    piece = None
    colour = None
    if Board.turn == Colour.WHITE:
        colour = "w"
    else:
        colour = "b"
    if num == 0:
        piece = (Board.turn, PieceType.ROOK, colour + "-rook")
        
    elif num == 1:
        piece = (Board.turn, PieceType.KNIGHT, colour + "-knight")
    elif num == 2:
        piece = (Board.turn, PieceType.BISHOP, colour + "-bishop")
    elif num == 3:
        piece = (Board.turn, PieceType.QUEEN, colour + "-queen")
    elif num == 4:
        piece = (Board.turn, PieceType.PAWN, colour + "-pawn")

    Board.promotion_menu_sqrs.remove(sqr)

    Board.activePieces[sqr] = piece
    sqrColour = Board.get_square_colour(sqr)
    draw_empty_square(gameDisplay, sqr, sqrColour)
    draw_piece(gameDisplay, piece, sqr)