import PieceType
import Board
from Colour import Colour
from PieceType import PieceType

# Checks if pawn at position sqr can perform en passant on the pawn at passingPieceSqr
def check_en_passant(sqr, passingPieceSqr):
    move = 0
    if Board.turn == Colour.WHITE:
        move = 1
    else:
        move = -1

    xPosNum = ord(sqr[0])
    passingPieceXNum = ord(passingPieceSqr[0])
    if passingPieceSqr[0] != "a":
        if passingPieceXNum - xPosNum == 1 and sqr[1] == passingPieceSqr[1]:
            enPassantPos = (passingPieceSqr[0], passingPieceSqr[1] + move)
            if not Board.has_chess_piece(enPassantPos):
                Board.enPassantMove = enPassantPos
            else:
                return

    if passingPieceSqr[0] != "h":
        if passingPieceXNum - xPosNum == -1 and sqr[1] == passingPieceSqr[1]:
            enPassantPos = (passingPieceSqr[0], passingPieceSqr[1] + move)
            if not Board.has_chess_piece(enPassantPos):
                Board.enPassantMove = enPassantPos
            else:
                return


# Gets all of the moves that a pawn can make from sqr
def get_pawn_moves(pawnSqr):
    pawn = Board.activePieces[pawnSqr]
    legalMoves = []
    move = 0
    edgeOfBoard = 0
    if pawn[0] == Colour.WHITE:
        move = 1
        edgeOfBoard = 9

        # If pawn is at initial position then pawn can move 2 steps
        if pawnSqr[1] == 2 and not Board.has_chess_piece((pawnSqr[0], pawnSqr[1] + 1)) and not Board.has_chess_piece((pawnSqr[0], pawnSqr[1] + 2)):
            twoSqrMove = (pawnSqr[0], pawnSqr[1]+2)
            legalMoves.append(twoSqrMove)
            Board.wPassingPiecePos = (pawnSqr[0], pawnSqr[1]+2)

        if len(Board.bPassingPiecePos) > 0:
            check_en_passant(pawnSqr, Board.bPassingPiecePos)
    else:
        move = -1
        edgeOfBoard = 0

        # If pawn is at initial position then pawn can move 2 steps
        if pawnSqr[1] == 7 and not Board.has_chess_piece((pawnSqr[0], pawnSqr[1] - 1)) and not Board.has_chess_piece((pawnSqr[0], pawnSqr[1] - 2)):
            legalMoves.append((pawnSqr[0], pawnSqr[1]-2))
            Board.bPassingPiecePos = (pawnSqr[0], pawnSqr[1]-2)

        # Check for en passant for black player
        if len(Board.wPassingPiecePos) > 0:
            check_en_passant(pawnSqr, Board.wPassingPiecePos)

                


    # Checks for moves that move forward
    if pawnSqr[1]+move != edgeOfBoard and not Board.has_chess_piece((pawnSqr[0], pawnSqr[1]+move)):
        legalMoves.append((pawnSqr[0], pawnSqr[1]+move))
    
    sidePos = []
    # Checks attacking angles
    xPos = ord(pawnSqr[0]) - 97
    if pawnSqr[0] != "a":
        leftXPos = chr((xPos-1) + 97)
        leftPos = (leftXPos, pawnSqr[1] + move)
        sidePos.append(leftPos)

    if pawnSqr[0] != "h":
        rightXPos = chr((xPos+1) + 97)
        rightPos = (rightXPos, pawnSqr[1] + move)
        sidePos.append(rightPos)
    
    
    for pawnSqr in sidePos:
        if Board.has_chess_piece(pawnSqr):
            piece = Board.activePieces[pawnSqr]
            if pawn[0] != piece[0]:
                legalMoves.append(pawnSqr)

    return legalMoves



# Gets all legal moves for the rook
def get_rook_moves(rookSqr):
    rook = Board.activePieces[rookSqr]
    legalMoves = []

    # Finds legal moves above and below the rook
    count = 0
    move = 1
    start = rookSqr[1] + move
    end = 9
    while count < 2:
        for i in range(start, end, move):
            square = (rookSqr[0], i)
            if not Board.has_chess_piece(square):
                legalMoves.append(square)
            else:
                piece = Board.activePieces[square]
                if rook[0] != piece[0]:
                    legalMoves.append(square)
                    break
                else:
                    break
        count += 1
        move = -1
        start = rookSqr[1] + move
        end = 0

    #  Finds legal moves on the left and right of the rook
    count = 0
    move = 1
    start = ord(rookSqr[0]) - 97 + move
    end = 8
    while count < 2:
        for i in range(start, end, move):
            square = (chr(i + 97), rookSqr[1])
            if not Board.has_chess_piece(square):
                legalMoves.append(square)
            else:
                piece = Board.activePieces[square]
                if rook[0] != piece[0]:
                    legalMoves.append(square)
                    break
                else:
                    break
        count += 1
        move = -1
        start = ord(rookSqr[0]) - 97 + move
        end = -1
    
    return legalMoves


# Gets all the moves for the knight at sqr
def get_knight_moves(knightSqr):
    knight = Board.activePieces[knightSqr]
    legalMoves = []
    
    # Checks for legal moves that are 2 squares above the knight
    # Checks if knight is at least 3 squares below the top of the board
    if knightSqr[1] + 2 <= 8:
        # You can map the letters a - h to 0 - 7 by getting the char's unicode and subtracting 97
        xNum = ord(knightSqr[0]) - 97

        # Checks if knight is at the left side of board
        if knightSqr[0] != "a":
            leftX = chr(xNum + 96)
            move = (leftX, knightSqr[1] + 2)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)
        
        # Checks if knight is at the right side of board
        if knightSqr[0] != "h":
            rightX = chr(xNum + 98)
            move = (rightX, knightSqr[1] + 2)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)

    # Checks if the knight is at least 3 squares above the bottom of the board
    if knightSqr[1] - 2 >= 1:
        xNum = ord(knightSqr[0]) - 97

        # Checks if knight is at the left side of board
        if knightSqr[0] != "a":
            leftX = chr(xNum + 96)
            move = (leftX, knightSqr[1] - 2)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)
        
        # Checks if knight is at the right side of board
        if knightSqr[0] != "h":
            rightX = chr(xNum + 98)
            move = (rightX, knightSqr[1] - 2)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)
            

    # Checks if the knight is at least 2 squares below the top of the board
    if knightSqr[1] + 1 <= 8:
        xNum = ord(knightSqr[0]) - 97

        if knightSqr[0] != "a" and knightSqr[0] != "b":
            leftX = chr(xNum + 95)
            move = (leftX, knightSqr[1] + 1)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)

        if knightSqr[0] != "g" and knightSqr[0] != "h":
            rightX = chr(xNum + 99)
            move = (rightX, knightSqr[1] + 1)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)
            
    

    # Checks if the knight is at least 2 squares above the bottom of the board
    if knightSqr[1] - 1 >= 1:
        xNum = ord(knightSqr[0]) - 97

        if knightSqr[0] != "a" and knightSqr[0] != "b":
            leftX = chr(xNum + 95)
            move = (leftX, knightSqr[1] - 1)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)
            

        if knightSqr[0] != "g" and knightSqr[0] != "h":
            rightX = chr(xNum + 99)
            move = (rightX, knightSqr[1] - 1)
            if not Board.has_chess_piece(move):
                legalMoves.append(move)
            else:
                piece = Board.activePieces[move]
                if knight[0] != piece[0]:
                    legalMoves.append(move)
            

    return legalMoves


def get_bishop_moves(bishopSqr):
    bishop = Board.activePieces[bishopSqr]

    legalMoves = []
    x = ord(bishopSqr[0]) - 96 # Maps a - h to 1 - 8
    y = bishopSqr[1]
    quadrant = 1
    moveUp = 0
    moveRight = 0
    xLimit = 0
    yLimit = 0

    while quadrant < 5:
        if quadrant == 1:
            moveUp = 1
            moveRight = 1
            xLimit = 8
            yLimit = 8

        if quadrant == 2:
            moveUp = 1
            moveRight = -1
            xLimit = 1
            yLimit = 8

        if quadrant == 3:
            moveUp = -1
            moveRight = -1
            xLimit = 1
            yLimit = 1

        if quadrant == 4:
            moveUp = -1
            moveRight = 1
            xLimit = 8
            yLimit = 1

        xDif = abs(xLimit - x)
        yDif = abs(yLimit - y)
        end = 0
        if xDif < yDif:
            end = xDif
        else:
            end = yDif

        for i in range(1, end+1):
            newY = bishopSqr[1] + (moveUp * i)
            xChar = chr(x + (moveRight * i) + 96)
            square = (xChar, newY)
            if Board.has_chess_piece(square):
                piece = Board.activePieces[square]
                if bishop[0] != piece[0]:
                    legalMoves.append(square)
                break
            else:
                legalMoves.append(square)

        quadrant += 1
    return legalMoves


def get_queen_moves(pos):
    legalMoves = []
    legalMoves = get_bishop_moves(pos)
    legalMoves = legalMoves + get_rook_moves(pos)
    return legalMoves


def get_king_moves(kingSqr, checkForCheck):
    king = Board.activePieces[kingSqr]

    legalMoves = []
    xStart = 0
    yStart = 0
    xEnd = 0
    yEnd = 0

    if kingSqr[0] != "a":
        xStart = -1
    if kingSqr[0] != "h":
        xEnd = 1

    if kingSqr[1] != 8:
        yStart = 1
    if kingSqr[1] != 1:
        yEnd = -1

    for x in range(xStart, xEnd+1):
        for y in range(yStart, yEnd-1, -1):
            if x != 0 or y != 0: 
                yChar = chr(ord(kingSqr[0]) + x)
                sqr = (yChar, kingSqr[1] + y)
                if not Board.has_chess_piece(sqr):
                    if checkForCheck and not check_for_check(sqr):
                        legalMoves.append(sqr)
                else:
                    piece = Board.activePieces[sqr]
                    if king[0] != piece[0] and checkForCheck and not check_for_check(sqr):
                        legalMoves.append(sqr)



    return legalMoves



def check_for_check(kingPos):
    for item in Board.activePieces.items():
        piece = item[1]
        if piece[0] != Board.turn:
            pos = item[0]
            moves = get_legal_moves(piece, pos, False, None)
            if kingPos in moves:
                return pos
    return None
            


#  Gets all the legal moves piece can make
def get_legal_moves(piece, pos, checkForCheck, checker):
    Board.enPassantMove = None

    # Turns the ability for en passant to happen off if the player that moved their pawn 2 squares moves again
    if Board.turn == Colour.WHITE and len(Board.wPassingPiecePos) > 0:
        Board.wPassingPiecePos = ()
    elif Board.turn == Colour.BLACK and len(Board.bPassingPiecePos) > 0:
        Board.bPassingPiecePos = ()

    legalMoves = []
    if piece[1] == PieceType.PAWN:
        legalMoves = get_pawn_moves(pos)
    elif piece[1] == PieceType.ROOK:
        legalMoves = get_rook_moves(pos)
    elif piece[1] == PieceType.KNIGHT:
        legalMoves = get_knight_moves(pos)
    elif piece[1] == PieceType.BISHOP:
        legalMoves = get_bishop_moves(pos)
    elif piece[1] == PieceType.QUEEN:
        legalMoves = get_queen_moves(pos)
    elif piece[1] == PieceType.KING:
        legalMoves = get_king_moves(pos, checkForCheck)

    if checker != None and piece[1] != PieceType.KING:
        if checker in legalMoves:
            legalMoves = [checker]
        else:
            legalMoves = []
    return legalMoves