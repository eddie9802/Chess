import Board
import Move
from Colour import Colour


def receive_move(selectedSqr, nextSqr, piece):
    Board.selected_sqr = selectedSqr
    checker = Board.get_checker_piece()
    legalMoves, passingPiecePos, enPassantMove = Move.get_legal_moves(piece, selectedSqr, True, checker)
    Board.legalMoves = legalMoves
    Board.enPassantMove = enPassantMove
    if Board.turn == Colour.WHITE:
        Board.wPassingPiecePos = passingPiecePos
    else:
        Board.bPassingPiecePos = passingPiecePos
    Board.check_if_move_is_legal(nextSqr)
