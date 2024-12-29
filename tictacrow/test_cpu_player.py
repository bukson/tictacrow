import pytest

from cpuplayer import minimax
from tictactoe import Board, TicTacToeBoard


def test_cpu_player():
    board = TicTacToeBoard()
    _minimax = minimax(board, True)
    assert _minimax == 0


def test_cpu_player_X_winning():
    board = TicTacToeBoard()
    (
        board.update_board([0, 0], 'X')
        .update_board([2, 2], 'O')
        .update_board([0, 1], 'X')
        .update_board([1, 1], 'O')
    )
    _minimax = minimax(board, True)
    assert _minimax == 1
