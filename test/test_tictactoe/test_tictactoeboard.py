import pytest

from board import Field, SYMBOL
from tictactoe.tictactoeboard import TicTacToeBoard


@pytest.mark.parametrize('fields, player, winner', [
    ([[0, 0], [1, 1], [2, 2]], SYMBOL.X, SYMBOL.X),
    ([[0, 2], [1, 1], [2, 0]], SYMBOL.O, SYMBOL.O),
    ([[0, 2], [1, 2], [2, 2]], SYMBOL.O, SYMBOL.O),
    ([[0, 1], [1, 1], [2, 1]], SYMBOL.X, SYMBOL.X),
    ([], SYMBOL.X, None),
])
def test_get_winning_player(fields: list[Field], player: SYMBOL, winner: SYMBOL) -> None:
    board = TicTacToeBoard()
    print(board)
    for field in fields:
        board.update_board(field, player)
    assert board.get_winning_player() == winner
