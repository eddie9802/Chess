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


# Removes the selection from the selected square
def remove_selection(gameDisplay):
    selected_sqr = Board.selected_sqr
    if selected_sqr != None:
        x = ord(selected_sqr[0]) - 97
        y = 8 - selected_sqr[1]
        colour = Board.get_square_colour(selected_sqr)
        rect = pygame.Rect(x * Board.sqr_length, y * Board.sqr_length, Board.sqr_length, Board.sqr_length)
        pygame.draw.rect(gameDisplay, colour, rect)


        piece_path = "./Images/pieces/01_classic/" + Board.activePieces[selected_sqr][2] + ".png"
        image = pygame.transform.scale(pygame.image.load(piece_path), (Board.sqr_length, Board.sqr_length))
        gameDisplay.blit(image, (x * Board.sqr_length, y * Board.sqr_length))

        Board.selected_sqr = None




# Draws a square around the selected square of the chess board
def draw_selection(gameDisplay, square):
    x = ord(square[0]) - 97
    y = 8 - square[1]

    # Removes the selection from the previously selected square
    remove_selection(gameDisplay)

    # Draws a border around a square by drawing two overlapping squares
    rect1 = pygame.Rect(x * Board.sqr_length, y * Board.sqr_length, Board.sqr_length, Board.sqr_length)
    aqua_blue = pygame.Color(40, 113, 134)
    pygame.draw.rect(gameDisplay, aqua_blue, rect1)


    tenth = math.floor(Board.sqr_length / 10)
    twentieth = math.floor(Board.sqr_length / 20)
    rect2 = pygame.Rect(x * Board.sqr_length + twentieth, y * Board.sqr_length + twentieth, Board.sqr_length - tenth, Board.sqr_length - tenth)
    rect2_colour = Board.get_square_colour(square)
    pygame.draw.rect(gameDisplay, rect2_colour, rect2)

    piece_path = "./Images/pieces/01_classic/" + Board.activePieces[square][2] + ".png"
    image = pygame.transform.scale(pygame.image.load(piece_path), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (x * Board.sqr_length, y * Board.sqr_length))


# Draws piece at square
def draw_piece(gameDisplay, piece, square):
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/" + piece[2] + ".png"), (Board.sqr_length, Board.sqr_length))
    x = ord(square[0]) - 97 # Gets the x axis value of the piece

    y = 8 - square[1]
    gameDisplay.blit(image, (x * Board.sqr_length, y * Board.sqr_length))


# Draws an empty square at the position square
def draw_empty_square(gameDisplay, square, colour):
    x = ord(square[0]) - 97
    y = 8 - square[1]

    rect = pygame.Rect(x * Board.sqr_length, y * Board.sqr_length, Board.sqr_length, Board.sqr_length)
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
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-rook.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (0,0))
    gameDisplay.blit(image, (length * 7, 0))

    # Draws black knights
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-knight.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (Board.sqr_length,0))
    gameDisplay.blit(image, (length * 6, 0))

    # Draws black bishops
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-bishop.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 2,0))
    gameDisplay.blit(image, (length * 5, 0))

    # Draws black queen
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-queen.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 3,0))

    # Draws black king
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-king.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 4,0))

    # Draws black pawn
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/b-pawn.png"), (Board.sqr_length, Board.sqr_length))
    for x in range(8):
        gameDisplay.blit(image, (x * Board.sqr_length,Board.sqr_length))

    
    # Draws all white pieces

    # Draws white rooks
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-rook.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (0, length * 7))
    gameDisplay.blit(image, (length * 7, length * 7))

    # Draws white knights
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-knight.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (Board.sqr_length, length * 7))
    gameDisplay.blit(image, (length * 6, length * 7))

    # Draws white bishops
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-bishop.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 2, length * 7))
    gameDisplay.blit(image, (length * 5, length * 7))

    # Draws white queen
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-queen.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 3, length * 7))

    # Draws white king
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-king.png"), (Board.sqr_length, Board.sqr_length))
    gameDisplay.blit(image, (length * 4, length * 7))

    # Draws white pawn
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/w-pawn.png"), (Board.sqr_length, Board.sqr_length))
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


def draw_menu_selection(gameDisplay, sqr, pos):
    sqr_length_fifth = Board.sqr_length / 5
    y = (8 - sqr[1]) * Board.sqr_length
    offset = pos[1] - y
    num = math.floor(offset / sqr_length_fifth)
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

    # Updates active pieces, and draws the piece onto its new position
    Board.activePieces[sqr] = piece
    sqrColour = Board.get_square_colour(sqr)
    draw_empty_square(gameDisplay, sqr, sqrColour)
    draw_piece(gameDisplay, piece, sqr)


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
            ptext.draw("White wins!", (20, (boardLength / 2) - (boardLength / 8)), fontsize = boardLength / 8, color=(255, 0, 0))
        else:
            ptext.draw("Black wins!", (20, (boardLength / 2) - (boardLength / 8)), fontsize = boardLength / 8, color=(255, 0, 0))


