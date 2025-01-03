import pytest

from board import SYMBOL
from tictactoe.cpuplayer import minimax
from tictactoe.tictactoeboard import TicTacToeBoard


def test_cpu_player():
    board = TicTacToeBoard()
    _minimax = minimax(board, True)
    assert _minimax == 0


def test_cpu_player_X_winning():
    board = TicTacToeBoard()
    (
        board.update_board([0, 0], SYMBOL.X)
        .update_board([2, 2], SYMBOL.O)
        .update_board([0, 1], SYMBOL.X)
        .update_board([1, 1], SYMBOL.O)
    )
    _minimax = minimax(board, True)
    assert _minimax == 1
