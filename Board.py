import array
import math

import Move
import Draw
from Colour import Colour
from PieceType import PieceType

# These global variables will be initialised in the function init
pygame = None
GAME_DISPLAY = None

# Square on the chess board that has been selected
selected_sqr = None

highlightsOn = False
promotion_menu_sqrs = []

# The colour of the player who is taking their turn
turn = Colour.WHITE

legalMoves = [] # All the legal moves that the selected piece can make
enPassantMove = None

# The positions of the white and black pawns that have just moved two squares
wPassingPiecePos = ()
bPassingPiecePos = ()

wKingPos = ()
bKingPos = ()

wKingMoved = False
bKingMoved = False

sqr_length = 100



def get_all_pieces():
    allPieces = {}

    blackPawn = (Colour.BLACK, PieceType.PAWN, "b-pawn")
    blackRook = (Colour.BLACK, PieceType.ROOK, "b-rook")
    blackKnight = (Colour.BLACK, PieceType.KNIGHT, "b-knight")
    blackBishop = (Colour.BLACK, PieceType.BISHOP, "b-bishop")
    blackQueen = (Colour.BLACK, PieceType.QUEEN, "b-queen")
    blackKing = (Colour.BLACK, PieceType.KING, "b-king")
    
    # Adds black pieces to dictionary
    allPieces[("a", 7)] = blackPawn
    allPieces[("b", 7)] = blackPawn
    allPieces[("c", 7)] = blackPawn
    allPieces[("d", 7)] = blackPawn
    allPieces[("e", 7)] = blackPawn
    allPieces[("f", 7)] = blackPawn
    allPieces[("g", 7)] = blackPawn
    allPieces[("h", 7)] = blackPawn

    allPieces[("a", 8)] = blackRook
    allPieces[("h", 8)] = blackRook

    allPieces[("b", 8)] = blackKnight
    allPieces[("g", 8)] = blackKnight

    allPieces[("c", 8)] = blackBishop
    allPieces[("f", 8)] = blackBishop

    allPieces[("d", 8)] = blackQueen
    allPieces[("e", 8)] = blackKing


    whitePawn = (Colour.WHITE, PieceType.PAWN, "w-pawn")
    whiteRook = (Colour.WHITE, PieceType.ROOK, "w-rook")
    whiteKnight = (Colour.WHITE, PieceType.KNIGHT, "w-knight")
    whiteBishop = (Colour.WHITE, PieceType.BISHOP, "w-bishop")
    whiteQueen = (Colour.WHITE, PieceType.QUEEN, "w-queen")
    whiteKing = (Colour.WHITE, PieceType.KING, "w-king")

    # Adds white pieces to dictionary
    allPieces[("a", 2)] = whitePawn
    allPieces[("b", 2)] = whitePawn
    allPieces[("c", 2)] = whitePawn
    allPieces[("d", 2)] = whitePawn
    allPieces[("e", 2)] = whitePawn
    allPieces[("f", 2)] = whitePawn
    allPieces[("g", 2)] = whitePawn
    allPieces[("h", 2)] = whitePawn

    allPieces[("a", 1)] = whiteRook
    allPieces[("h", 1)] = whiteRook

    allPieces[("b", 1)] = whiteKnight
    allPieces[("g", 1)] = whiteKnight

    allPieces[("c", 1)] = whiteBishop
    allPieces[("f", 1)] = whiteBishop

    allPieces[("d", 1)] = whiteQueen
    allPieces[("e", 1)] = whiteKing

    global wKingPos
    global bKingPos
    wKingPos = ("e", 1)
    bKingPos = ("e", 8)

    return allPieces

# Active pieces holds all of the pieces that are currently on the chess board.  It is a dictionary that is index by the pieces position
# Is initialised by the set_up_board function
activePieces = get_all_pieces()


# Takes a sqr and determines the position of that square 
def get_square_colour(sqr):
    x = ord(sqr[0]) - 97 # Gets the unicode value of the x part of the squares position
    if x % 2 == 0:
        if sqr[1] % 2 == 0:
            return Draw.WHITE
        else:
            return Draw.BLACK
    else:
        if sqr[1] % 2 == 0:
            return Draw.BLACK
        else:
            return Draw.WHITE


# Checks if square has a chess piece on it
def has_chess_piece(square_pos):
    if activePieces.get(square_pos) == None:
        return False
    else:
        return True


# Determines if the piece is a friendly piece
def is_friendly_piece(piece):
    if turn == piece[0]:
        return True
    else:
        return False


# Promotes a pawn
def promote_pawn(pos):
    sqr = get_sqr_from_xy(pos) # Gets window xy coordinates
    
    if has_chess_piece(sqr):
        piece = activePieces[sqr]

        # Determines if the piece that was right clicked on was a pawn and the pawn is at the end of its run
        if (turn == piece[0] and ((Colour.WHITE == piece[0] and piece[1] == PieceType.PAWN and sqr[1] == 8) or 
            (Colour.BLACK == piece[0] and piece[1] == PieceType.PAWN  and sqr[1] == 1))):
            Draw.draw_promotion_menu(GAME_DISPLAY, sqr)
    


# Sets the global varaible turn to the other colour
def change_turn():
    global turn
    if turn == Colour.WHITE:
        turn = Colour.BLACK
    else:
        turn = Colour.WHITE


# Removes all the highlights from the on screen board
# The highlighted squares will be all the legal moves a piece can make as well as any enpassant moves
def get_highlighted_sqrs():
    highlighted_sqrs = [] + legalMoves
    if enPassantMove != None:
        highlighted_sqrs.append(enPassantMove)
    return highlighted_sqrs




# Makes the piece specified by selected square to the square position
def move_piece(square):
    global turn
    global enPassantMove
    global bKingPos
    global wKingPos
    global highlightsOn
    global selected_sqr
    global bKingMoved
    global wKingMoved


    for move in legalMoves:
        if square == move:
            # Sets the global king pos if the selected square was a king
            if selected_sqr == bKingPos:
                bKingPos = square
                if not bKingMoved:
                    bKingMoved = True
            elif selected_sqr == wKingPos:
                wKingPos = square
                if not wKingMoved:
                    wKingMoved = True

            piece = activePieces[selected_sqr]
            activePieces[square] = piece # Make the enemy pieces position equal to piece
            selSquare = selected_sqr
            Draw.remove_selection(GAME_DISPLAY)
            del activePieces[selSquare]
            colour = get_square_colour(square)
            Draw.draw_empty_square(GAME_DISPLAY, square, colour)
            Draw.draw_piece(GAME_DISPLAY, piece, square)
            colour2 = get_square_colour(selSquare)
            Draw.draw_empty_square(GAME_DISPLAY, selSquare, colour2)
            change_turn()
            enPassantMove = None

            Draw.remove_all_highlights(GAME_DISPLAY)
            highlightsOn = False
            
    # Check for en passant move
    if square == enPassantMove:
        enemySqr = None
        if turn == Colour.WHITE:
            enemySqr = (enPassantMove[0], enPassantMove[1] - 1)
        else:
            enemySqr = (enPassantMove[0], enPassantMove[1] + 1)
        piece = activePieces[selected_sqr]
        activePieces[square] = piece
        selSquare = selected_sqr
        Draw.remove_selection(GAME_DISPLAY)
        del activePieces[selSquare]
        Draw.draw_piece(GAME_DISPLAY, piece, square)
        colour1 = get_square_colour(selSquare)
        colour2 = get_square_colour(enemySqr)
        Draw.draw_empty_square(GAME_DISPLAY, selSquare, colour1)
        Draw.draw_empty_square(GAME_DISPLAY, enemySqr, colour2)
        change_turn()

        Draw.remove_all_highlights(GAME_DISPLAY)
        highlightsOn = False
        enPassantMove = None
    
    selected_sqr = None


def get_sqr_xy(sqr):
    x = ord(sqr[0]) - 97
    y = (8 - (sqr[1] - 1)) - 1
    return x, y
            

def get_sqr_from_xy(pos):
    x = pos[0]
    # This inverts the y value because in chess the y number increases from bottom to top
    y = (sqr_length * 8) - pos[1]

    xPos = math.floor(x / sqr_length)
    yPos = math.floor(y / sqr_length)

    # The square the user clicked on is found and the store is denoted by a letter and a number in a tuple
    square = (chr(xPos + 97), yPos + 1)
    return square

# Selects the square that was clicked on.  If user clicks on a friend piece then that piece is selected to move.  If user picks a square that does
# not have a friendly piece then the user will either move to that square or attack the enemy square if the move was legal
def select_square(pos):
    square = get_sqr_from_xy(pos)

    if square in promotion_menu_sqrs:
        Draw.draw_menu_selection(GAME_DISPLAY, square, pos)
    else:
        global selected_sqr
        if has_chess_piece(square):
            clickedPiece = activePieces[square]

            # If square has a friendly piece then select square
            if is_friendly_piece(clickedPiece):
                if highlightsOn:
                    Draw.remove_all_highlights(GAME_DISPLAY)
                Draw.draw_selection(GAME_DISPLAY, square)
                selected_sqr = square
                # check if square user has clicked on is a legal move
                selectedPiece = activePieces[selected_sqr]
                global legalMoves
                Move.check_for_check()
                legalMoves = Move.get_legal_moves(selectedPiece, selected_sqr)
                sqrs_to_highlight = get_highlighted_sqrs()
                for sqr in sqrs_to_highlight:
                    Draw.highlight_square(GAME_DISPLAY, sqr)

            # Clicked on square has an enemy piece.  Check if a friend square has been selected to attack this piece
            elif selected_sqr != None:
                move_piece(square)

        elif selected_sqr != None:
            move_piece(square)


def white_castle(rookSqr, newRookSqr, newKingSqr):
    global wKingPos

    wKing = activePieces[wKingPos]

    # Draws empty square where king used to be
    colour = get_square_colour(wKingPos)
    Draw.draw_empty_square(GAME_DISPLAY, wKingPos, colour)

    del activePieces[wKingPos]
    activePieces[newKingSqr] = wKing

    # Draws king in new position
    Draw.draw_piece(GAME_DISPLAY, wKing, newKingSqr)

    # Draws empty square where the rook used to be
    colour = get_square_colour(rookSqr)
    Draw.draw_empty_square(GAME_DISPLAY, rookSqr, colour)

    rook = activePieces[rookSqr]

    del activePieces[rookSqr]
    activePieces[newRookSqr] = rook

    # Draws rook in new position
    Draw.draw_piece(GAME_DISPLAY, rook, newRookSqr)
    Draw.remove_all_highlights(GAME_DISPLAY)


def black_castle(rookSqr, newRookSqr, newKingSqr):
    global bKingPos

    wKing = activePieces[bKingPos]

    # Draws empty square where king used to be
    colour = get_square_colour(bKingPos)
    Draw.draw_empty_square(GAME_DISPLAY, bKingPos, colour)

    del activePieces[bKingPos]
    activePieces[newKingSqr] = wKing

    # Draws king in new position
    Draw.draw_piece(GAME_DISPLAY, wKing, newKingSqr)

    # Draws empty square where the rook used to be
    colour = get_square_colour(rookSqr)
    Draw.draw_empty_square(GAME_DISPLAY, rookSqr, colour)

    rook = activePieces[rookSqr]

    del activePieces[rookSqr]
    activePieces[newRookSqr] = rook

    # Draws rook in new position
    Draw.draw_piece(GAME_DISPLAY, rook, newRookSqr)
    Draw.remove_all_highlights(GAME_DISPLAY)


def castle(pos):
    global wKingPos
    global bKingPos
    global selected_sqr
    global turn


    sqr = get_sqr_from_xy(pos)
    if has_chess_piece(sqr):
        piece = activePieces[sqr]
        if piece[1] == PieceType.ROOK and piece[0] == turn:
            if piece[0] == Colour.WHITE and not wKingMoved and selected_sqr == wKingPos:
                if sqr == ("a", 1) and not has_chess_piece(("b", 1)) and not has_chess_piece(("c", 1)):
                    white_castle(sqr, ("c", 1), ("b", 1))

                elif sqr == ("h", 1) and not has_chess_piece(("f", 1)) and not has_chess_piece(("g", 1)):
                    white_castle(sqr, ("f", 1), ("g", 1))
            else:
                if sqr == ("a", 8) and not has_chess_piece(("b", 8)) and not has_chess_piece(("c", 8)):
                    black_castle(sqr, ("c", 8), ("b", 8))

                elif sqr == ("h", 8) and not has_chess_piece(("f", 8)) and not has_chess_piece(("g", 8)):
                    black_castle(sqr, ("f", 8), ("g", 8))
        selected_sqr = None
        Draw.remove_selection(GAME_DISPLAY)
        if turn == Colour.WHITE:
            turn = Colour.BLACK
        else:
            turn = Colour.WHITE

        
             

    

# Initialises pygame and GAME_DISPLAY and sets up the initial board
def init(gameDisplay):
    global GAME_DISPLAY
    GAME_DISPLAY = gameDisplay
    Draw.draw_empty_board(GAME_DISPLAY) # Draws an empty board
    Draw.populate_board(GAME_DISPLAY) # Fills the empty board



