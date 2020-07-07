import array
import math

import Move
from Colour import Colour
from PieceType import PieceType

# These global variables will be initialised in the function init
pygame = None
gameDisplay = None
# Colours of the chess board
beige = None
gray = None
orange = None

# Square on the chess board that has been selected
selectedSquare = ()

# Active pieces holds all of the pieces that are currently on the chess board.  It is a dictionary that is index by the pieces position
# Is initialised by the set_up_board function
activePieces = None
unactivePieces = {}

# The colour of the player who is taking their turn
turn = Colour.WHITE

legalMoves = [] # All the legal moves that the selected piece can make
enPassantMove = ()

# The positions of the white and black pawns that have just moved two squares
wPassingPiecePos = ()
bPassingPiecePos = ()

wKingPos = ()
bKingPos = ()



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


# Fills the chess board
def populate_board():
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


# Takes a square's position and determines the colour of that square
def get_square_colour(sqr):
    x = ord(sqr[0]) - 97
    if x % 2 == 0:
        if sqr[1] % 2 == 0:
            return beige
        else:
            return gray
    else:
        if sqr[1] % 2 == 0:
            return gray
        else:
            return beige


# Checks if square has a chess piece on it
def has_chess_piece(square_pos):
    if activePieces.get(square_pos) == None:
        return False
    else:
        return True


# Removes the selection from the selected square
def remove_selection():
    global selectedSquare
    if len(selectedSquare) > 0:
        x = ord(selectedSquare[0]) - 97
        y = (9 - selectedSquare[1]) - 1
        colour = get_square_colour(selectedSquare)
        rect = pygame.Rect(x * 100, y * 100, 100, 100)
        pygame.draw.rect(gameDisplay, colour, rect)


        piece_path = "./Images/pieces/01_classic/" + activePieces[selectedSquare][2] + ".png"
        image = pygame.transform.scale(pygame.image.load(piece_path), (100, 100))
        gameDisplay.blit(image, (x * 100, y * 100))

        selectedSquare = ()


# Determines if the piece is a friendly piece
def is_friendly_piece(piece):
    if turn == piece[0]:
        return True
    else:
        return False


# Draws a square around the selected square of the chess board
def draw_selection(square):
    x = ord(square[0]) - 97
    y = (9 - square[1]) - 1

    # Removes the selection from the previously selected square
    remove_selection()

    # Draws a border around a square by drawing two overlapping squares
    rect1 = pygame.Rect(x * 100, y * 100, 100, 100)
    aqua_blue = pygame.Color(40, 113, 134)
    pygame.draw.rect(gameDisplay, aqua_blue, rect1)

    rect2 = pygame.Rect(x * 100 + 5, y * 100 + 5, 90, 90)
    rect2_colour = get_square_colour(square)
    pygame.draw.rect(gameDisplay, rect2_colour, rect2)

    piece_path = "./Images/pieces/01_classic/" + activePieces[square][2] + ".png"
    image = pygame.transform.scale(pygame.image.load(piece_path), (100, 100))
    gameDisplay.blit(image, (x * 100, y * 100))


# Draws piece at square
def draw_piece(piece, square):
    image = pygame.transform.scale(pygame.image.load("./Images/pieces/01_classic/" + piece[2] + ".png"), (100, 100))
    x = ord(square[0]) - 97 # Gets the x axis value of the piece

    y = 8 - square[1]
    gameDisplay.blit(image, (x * 100, y * 100))


# Draws an empty square at the position square
def draw_empty_square(square, colour):
    x = ord(square[0]) - 97
    y = 8 - square[1]

    rect = pygame.Rect(x * 100, y * 100, 100, 100)
    pygame.draw.rect(gameDisplay, colour, rect)


# Sets the global varaible turn to the other colour
def change_turn():
    global turn
    if turn == Colour.WHITE:
        turn = Colour.BLACK
    else:
        turn = Colour.WHITE



# Makes the piece specified by selected square to the square position
def move_piece(square):
    global turn
    global enPassantMove
    global bKingPos
    global wKingPos

    for move in legalMoves:
        if square == move:

            # Sets the global king pos if the selected square was a king
            if selectedSquare == bKingPos:
                bKingPos = square
            elif selectedSquare == wKingPos:
                wKingPos = square

            piece = activePieces[selectedSquare]
            activePieces[square] = piece # Make the enemy pieces position equal to piece
            selSquare = selectedSquare
            remove_selection()
            del activePieces[selSquare]
            colour = get_square_colour(square)
            draw_empty_square(square, colour)
            draw_piece(piece, square)
            colour2 = get_square_colour(selSquare)
            draw_empty_square(selSquare, colour2)
            change_turn()
            return
            
    # Check for en passant move
    if square == enPassantMove:
        enemySqr = ()
        if turn == Colour.WHITE:
            enemySqr = (enPassantMove[0], enPassantMove[1] - 1)
        else:
            enemySqr = (enPassantMove[0], enPassantMove[1] + 1)
        piece = activePieces[selectedSquare]
        activePieces[square] = piece
        selSquare = selectedSquare
        remove_selection()
        del activePieces[selSquare]
        draw_piece(piece, square)
        colour1 = get_square_colour(selSquare)
        colour2 = get_square_colour(enemySqr)
        draw_empty_square(selSquare, colour1)
        draw_empty_square(enemySqr, colour2)
        change_turn()


def get_sqr_xy(sqr):
    x = ord(sqr[0]) - 97
    y = (8 - (sqr[1] - 1)) - 1
    return x, y


def highlight_square(sqr):
    #x, y = get_sqr_xy(sqr)
    #rect = pygame.Rect(100 * x, 100 * y)
    draw_empty_square(sqr, orange)
    if has_chess_piece(sqr):
        piece = activePieces[sqr]
        draw_piece(piece, sqr)



# Selects the square that was clicked on.  If user clicks on a friend piece then that piece is selected to move.  If user picks a square that does
# not have a friendly piece then the user will either move to that square or attack the enemy square if the move was legal
def select_square(pos):
    x = pos[0]
    # This inverts the y value because in chess the y number increases from bottom to top
    y = 800 - pos[1]

    xPos = math.floor(x / 100)
    yPos = math.floor(y / 100)



    # The square the user clicked on is found and the store is denoted by a letter and a number in a tuple
    square = (chr(xPos + 97), yPos + 1)

    global selectedSquare
    if has_chess_piece(square):
        clickedPiece = activePieces[square]

        # If square has a friendly piece then select square
        if is_friendly_piece(clickedPiece):
            draw_selection(square)
            selectedSquare = square
            # check if square user has clicked on is a legal move
            selectedPiece = activePieces[selectedSquare]
            global legalMoves
            Move.check_for_check()
            legalMoves = Move.get_legal_moves(selectedPiece, selectedSquare)
            for move in legalMoves:
                highlight_square(move)

        # Clicked on square has an enemy piece.  Check if a friend square has been selected to attack this piece
        elif len(selectedSquare) == 2:
            move_piece(square)

    elif len(selectedSquare) == 2:
        move_piece(square)


# Draws an empty board
def draw_empty_board():
    isBeige = False
    for x in range(8):
        isBeige = not isBeige
        for y in range(8):
            colour = None
            if isBeige:
                # Colours the square beige
                colour = beige
            else:
                # Colours the square gray
                colour = gray
            rect = pygame.Rect(x * 100, y * 100, 100, 100)
            pygame.draw.rect(gameDisplay, colour, rect)
            isBeige = not isBeige



# Places the the inital pieces into activePieces, draws an empty board, then populates it
def set_up_board():
    global activePieces
    activePieces = get_all_pieces() # Puts all initial pieces of a chess board into activePieces
    draw_empty_board() # Draws an empty board
    populate_board() # Fills the empty board

# Initialises pygame and gameDisplay and sets up the initial board
def init(pgame, gDisplay):
    global pygame
    global gameDisplay
    global beige
    global gray
    global orange
    pygame = pgame
    gameDisplay = gDisplay
    beige = pygame.Color(245,245,220)
    gray = pygame.Color(128,128,128)
    orange = pygame.Color(255,165,0)
    set_up_board()



