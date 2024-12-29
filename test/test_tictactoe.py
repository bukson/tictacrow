import pytest

from tictactoe import Board, TicTacToeBoard, Field


def test_get_valid_move_positions():
    board = Board(board_size=3, empty_value='_')
    valid_positions = board.get_valid_move_positions()
    assert len(valid_positions) == 9


@pytest.mark.parametrize('fields, player, winner', [
    ([[0, 0], [1, 1], [2, 2]], 'X', 'X'),
    ([[0, 2], [1, 1], [2, 0]], 'O', 'O'),
    ([[0, 2], [1, 2], [2, 2]], 'O', 'O'),
    ([[0, 1], [1, 1], [2, 1]], 'X', 'X'),
    ([], 'X', None),
])
def test_get_winning_player(fields: list[Field], player: str, winner: str) -> None:
    board = TicTacToeBoard()
    print(board)
    for field in fields:
        board.update_board(field, player)
    assert board.get_winning_player() == winner
