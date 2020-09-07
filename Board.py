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
wPassingPiecePos = None
bPassingPiecePos = None

wKingPos = ()
bKingPos = ()

wKingMoved = False
bKingMoved = False

sqr_length = 100

GAME_FINISHED = False
PLAYER_COLOUR = None



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
    if PLAYER_COLOUR == Colour.BLACK:
        invertedSqr = Draw.invertSqr(sqr)
        sqr = invertedSqr
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
def promote_pawn(sqr):
    global selected_sqr
    if selected_sqr != None:
        Draw.remove_selection_outline(GAME_DISPLAY)
    if highlightsOn:
        Draw.remove_all_highlights(GAME_DISPLAY)
    
    if has_chess_piece(sqr):
        piece = activePieces[sqr]

        # Determines if the piece that was right clicked on was a pawn and the pawn is at the end of its run
        if (turn == piece[0] and ((Colour.WHITE == piece[0] and piece[1] == PieceType.PAWN and sqr[1] == 8) or 
            (Colour.BLACK == piece[0] and piece[1] == PieceType.PAWN  and sqr[1] == 1))) and sqr not in promotion_menu_sqrs:
            Draw.draw_promotion_menu(GAME_DISPLAY, sqr)
            promotion_menu_sqrs.append(sqr)
    


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


def check_for_king_move(selectedSqr, newPos):
    """Checks if the king has moves from its position.
    If it has then a boolean for that king showing whether or not the king
    has moved is set to True."""
    global bKingPos
    global wKingPos
    global bKingMoved
    global wKingMoved

    # Sets the global king pos if the selected square was a king and sets the kingMoves boolean to true
    if selected_sqr[0] == bKingPos[0] and selected_sqr[1] == bKingPos[1]:
        bKingPos = newPos
        if not bKingMoved:
            bKingMoved = True
    elif selected_sqr[0] == wKingPos[0] and selected_sqr[1] == wKingPos[1]:
        wKingPos = newPos
        if not wKingMoved:
            wKingMoved = True
    

def move_piece(square):
    """Updates the dictionary, draws the piece unto its new position, removes the selection from the selected piece."""
    global selected_sqr
    global highlightsOn
    global enPassantMove
    global legalMoves
    
    # Sets the selected piece to its new position in the activePieces dictionary
    selectedPiece = activePieces[selected_sqr]
    activePieces[square] = selectedPiece # Sets the selected piece to the square that the piece is moving to

    # The the chess piece that is moving onto its new position
    newPosColour = get_square_colour(square)
    Draw.draw_empty_square(GAME_DISPLAY, square, newPosColour)
    Draw.draw_piece(GAME_DISPLAY, selectedPiece, square)

    # Fills the selected piece's old position with an empty square
    oldPosColour = get_square_colour(selected_sqr)
    Draw.draw_empty_square(GAME_DISPLAY, selected_sqr, oldPosColour)

    # Removes all the highlights for the piece's legal moves
    Draw.remove_all_highlights(GAME_DISPLAY)
    highlightsOn = False

    # Removes the piece that was in the selected square from the selected_sqr index
    del activePieces[selected_sqr]
    selected_sqr = None

    # Sets the enPassantMove and legalMoves to None and an empty array respectively
    enPassantMove = None
    legalMoves = []

    change_turn()


def find_enemy_enpassant_piece():
    """Finds the square the piece that is to be taken in the en passant move is on."""
    enemySqr = None
    if turn == Colour.WHITE:
        enemySqr = (enPassantMove[0], enPassantMove[1] - 1)
    else:
        enemySqr = (enPassantMove[0], enPassantMove[1] + 1)
    return enemySqr


def perform_enpassant(square):
    """Performs the en passant move to the square provided"""
    global enPassantMove
    global selected_sqr
    global highlightsOn
    global legalMoves

    # Sets the piece that is on the selected sqr to its new position in the activePieces dictionary
    selectedPiece = activePieces[selected_sqr]
    activePieces[square] = selectedPiece

    # Draws the selected piece unto its new position on the chess board
    Draw.draw_piece(GAME_DISPLAY, selectedPiece, square)

    # Draws an empty square where the selected piece used to be
    selectedSqrColour = get_square_colour(selected_sqr)
    Draw.draw_empty_square(GAME_DISPLAY, selected_sqr, selectedSqrColour)

    # Removes the enemy piece from its square on the chess board
    enemySqr = find_enemy_enpassant_piece()
    enemySqrColour = get_square_colour(enemySqr)
    Draw.draw_empty_square(GAME_DISPLAY, enemySqr, enemySqrColour)

    change_turn()

    Draw.remove_all_highlights(GAME_DISPLAY)
    highlightsOn = False

    # Removes the enemy
    del activePieces[selected_sqr]
    del activePieces[enemySqr]
    selected_sqr = None

    enPassantMove = None
    legalMoves = []


# Makes the piece specified by selected square to the square position
def check_if_move_is_legal(square):
    """Moves a piece from one place to the next"""
    global turn
    global bKingPos
    global wKingPos
    global highlightsOn
    global selected_sqr
    global bKingMoved
    global wKingMoved
    global legalMoves
    global selected_sqr


    for move in legalMoves:
        if square == move:
            check_for_king_move(select_square, square)
            move_piece(square)
            return "MoveMade"
            
    
    # Check for en passant move
    if square == enPassantMove:
        perform_enpassant(square)
        return "MoveMade"
    return "NoMoveMade"


def get_sqr_xy(sqr):
    x = (ord(sqr[0]) - 97) * sqr_length
    y = sqr_length * 8 - sqr[1] * sqr_length + 1
    return x, y
            

def get_sqr_from_xy(pos):
    """Takes a mouse click position and determines what square was clicked on.  Returns the square that was clicked on."""
    x = pos[0]
    square = None
    
    # This inverts the y value because in chess the y number increases from bottom to top
    y = (sqr_length * 8) - pos[1]

    xPos = math.floor(x / sqr_length)
    rank = chr(xPos + 97)
    sqrFile = math.floor(y / sqr_length) + 1 # 1 is added as files start from 1

    # The square the user clicked on is found and the store is denoted by a letter and a number in a tuple
    square = (rank, sqrFile)

    if PLAYER_COLOUR == Colour.BLACK and turn == Colour.BLACK:
        if x % sqr_length == 0 or x % sqr_length == sqr_length:
            x = x + 1
        # Inverts the rank and file of the square
        invertedX = (8 * sqr_length) - x
        invertedXPos = math.floor(invertedX / sqr_length)
        invertedRank = chr(invertedXPos + 97)
        invertedFile = 9 - sqrFile

        square = (invertedRank, invertedFile)
    return square


def get_checker_piece():
    global wPassingPiecePos
    global bPassingPiecePos

    checker = None
    if turn == Colour.WHITE:
        checker = Move.check_for_check(wKingPos, None)
    else:
        checker = Move.check_for_check(bKingPos, None)

    return checker


# Takes the use mouse click position and selects an item from the promotion menu
def select_promotion_menu_item(gameDisplay, sqr, pos):
    global turn
    retVal = "NoMoveMade"
    sqr_length_fifth = sqr_length / 5
    y = (8 - sqr[1]) * sqr_length
    offset = pos[1] - y
    num = math.floor(offset / sqr_length_fifth)
    piece = None
    colour = None
    if turn == Colour.WHITE:
        colour = "w"
    else:
        colour = "b"
    if num == 0:
        piece = (turn, PieceType.ROOK, colour + "-rook")
        retVal = "PawnPromoted"
        
    elif num == 1:
        piece = (turn, PieceType.KNIGHT, colour + "-knight")
        retVal = "PawnPromoted"
    elif num == 2:
        piece = (turn, PieceType.BISHOP, colour + "-bishop")
        retVal = "PawnPromoted"
    elif num == 3:
        piece = (turn, PieceType.QUEEN, colour + "-queen")
        retVal = "PawnPromoted"
    elif num == 4:
        piece = (turn, PieceType.PAWN, colour + "-pawn")
        retVal = "PawnPromoted"

    promotion_menu_sqrs.remove(sqr)

    # Updates active pieces, and draws the piece onto its new position
    activePieces[sqr] = piece
    sqrColour = get_square_colour(sqr)
    Draw.draw_empty_square(gameDisplay, sqr, sqrColour)
    Draw.draw_piece(gameDisplay, piece, sqr)

    if retVal == "PawnPromoted":
        if turn == Colour.WHITE:
            turn = Colour.BLACK
        else:
            turn = Colour.WHITE

    return retVal


# Selects the square that was clicked on.  If user clicks on a friend piece then that piece is selected to move.  If user picks a square that does
# not have a friendly piece then the user will either move to that square or attack the enemy square if the move was legal
def select_square(pos):
    global wPassingPiecePos
    global bPassingPiecePos
    global enPassantMove
    global selected_sqr
    square = get_sqr_from_xy(pos)
    if square in promotion_menu_sqrs:
        selected_sqr = None
        return select_promotion_menu_item(GAME_DISPLAY, square, pos)
    else:
        if has_chess_piece(square):
            clickedPiece = activePieces[square]

            # If square has a friendly piece then select square
            if is_friendly_piece(clickedPiece):
                if highlightsOn:
                    Draw.remove_all_highlights(GAME_DISPLAY)
                Draw.remove_promotion_menus(GAME_DISPLAY)
                Draw.draw_selection(GAME_DISPLAY, square)
                selected_sqr = square
                # check if square user has clicked on is a legal move
                selectedPiece = activePieces[selected_sqr]
                global legalMoves
                checker = get_checker_piece()
                # Turns the ability for en passant to happen off if the player that moved their pawn 2 squares moves again
                if turn == Colour.WHITE and wPassingPiecePos != None:
                    wPassingPiecePos = None
                elif turn == Colour.BLACK and bPassingPiecePos != None:
                    bPassingPiecePos = None
                legalMoves, passingPiecePos, enPassantMove = Move.get_legal_moves(selectedPiece, selected_sqr, True, checker)
                if turn == Colour.WHITE:
                    wPassingPiecePos = passingPiecePos
                else:
                    bPassingPiecePos = passingPiecePos
                enPassantMove = enPassantMove
                sqrs_to_highlight = get_highlighted_sqrs()
                for sqr in sqrs_to_highlight:
                    Draw.highlight_square(GAME_DISPLAY, sqr)

            # Clicked on square has an enemy piece.  Check if a friend square has been selected to attack this piece
            elif selected_sqr != None:
                return check_if_move_is_legal(square)

        elif selected_sqr != None:
            return check_if_move_is_legal(square)
    return "NoMoveMade"


def dict_to_list(dictionary):
    """Converts a dictionary to a list"""
    dictList = []
    for key, value in dictionary.items():
        dictList.append((key, value))
    return dictList


def check_for_checkmate():
    """Loops through all of the pieces of the player that is next to move and checks if any one of their pieces can move.
        If they can't then a checkmate has happened"""
    activePiecesList = dict_to_list(activePieces)
    checker = get_checker_piece()
    for elem in activePiecesList:
        sqr = elem[0]
        piece = elem[1]
        legalMoves, passingPiecePos, enPassantMove = Move.get_legal_moves(piece, sqr, True, checker)
        if piece[0] == turn and len(legalMoves) > 0:
            return False
    return True



def white_castle(rookSqr, newRookSqr, newKingSqr):
    global wKingPos
    global bKingPos
    global turn

    kingPiece = None
    kingPos = None
    if turn == Colour.WHITE:
        kingPos = wKingPos
        kingPiece = activePieces[wKingPos]
    else:
        kingPos = bKingPos
        kingPiece = activePieces[bKingPos]


    # Draws empty square where king used to be
    colour = get_square_colour(kingPos)
    Draw.draw_empty_square(GAME_DISPLAY, kingPos, colour)

    del activePieces[kingPos]
    activePieces[newKingSqr] = kingPiece

    # Draws king in new position
    Draw.draw_piece(GAME_DISPLAY, kingPiece, newKingSqr)

    # Draws empty square where the rook used to be
    colour = get_square_colour(rookSqr)
    Draw.draw_empty_square(GAME_DISPLAY, rookSqr, colour)

    rook = activePieces[rookSqr]

    del activePieces[rookSqr]
    activePieces[newRookSqr] = rook

    # Draws rook in new position
    Draw.draw_piece(GAME_DISPLAY, rook, newRookSqr)
    Draw.remove_all_highlights(GAME_DISPLAY)

    if turn == Colour.WHITE:
        turn = Colour.BLACK
    else:
        turn = Colour.WHITE


def black_castle(rookSqr, newRookSqr, newKingSqr):
    global bKingPos
    global turn

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

    if turn == Colour.WHITE:
        turn = Colour.BLACK
    else:
        turn = Colour.WHITE


def castle(sqr):
    global wKingPos
    global bKingPos
    global selected_sqr
    global turn

    retVal = "NoMoveMade"


    if has_chess_piece(sqr):
        piece = activePieces[sqr]
        if piece[1] == PieceType.ROOK and piece[0] == turn:
            if piece[0] == Colour.WHITE and not wKingMoved and selected_sqr == wKingPos:
                if sqr == ("a", 1) and not has_chess_piece(("b", 1)) and not has_chess_piece(("c", 1)):
                    Draw.remove_selection_outline(GAME_DISPLAY)
                    selected_sqr = None
                    white_castle(sqr, ("c", 1), ("b", 1))
                    retVal = "MoveMade"

                elif sqr == ("h", 1) and not has_chess_piece(("f", 1)) and not has_chess_piece(("g", 1)):
                    Draw.remove_selection_outline(GAME_DISPLAY)
                    selected_sqr = None
                    white_castle(sqr, ("f", 1), ("g", 1))
                    retVal = "MoveMade"

            elif piece[0] == Colour.BLACK and not bKingMoved and selected_sqr == bKingPos:
                if sqr == ("a", 8) and not has_chess_piece(("b", 8)) and not has_chess_piece(("c", 8)):
                    Draw.remove_selection_outline(GAME_DISPLAY)
                    selected_sqr = None
                    black_castle(sqr, ("c", 8), ("b", 8))
                    retVal = "MoveMade"

                elif sqr == ("h", 8) and not has_chess_piece(("f", 8)) and not has_chess_piece(("g", 8)):
                    Draw.remove_selection_outline(GAME_DISPLAY)
                    selected_sqr = None
                    black_castle(sqr, ("f", 8), ("g", 8))
                    retVal = "MoveMade"
    return retVal
        

        
             

    

# Initialises pygame and GAME_DISPLAY and sets up the initial board
def init(gameDisplay, playerColour):
    global GAME_DISPLAY
    global PLAYER_COLOUR
    GAME_DISPLAY = gameDisplay
    PLAYER_COLOUR = playerColour
    Draw.redraw_board(gameDisplay)



