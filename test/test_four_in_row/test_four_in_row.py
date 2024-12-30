import pytest

from board import Field
from four_in_row.board import FourInRowBoard


@pytest.mark.parametrize('fields, players, winner', [
    ([[0, 0], [1, 1], [2, 2]], ['X', 'X', 'X'], None),
    ([[0, 0], [1, 1], [2, 2], [3, 3]], ['X', 'X', 'X', 'X'], 'X'),
    ([[0, 0], [1, 1], [2, 2], [3, 3]], ['X', 'X', 'O', 'X'], None),
    ([[0, 2], [1, 1], [2, 0]], ['O', 'O', 'O'], None),
    ([[0, 3], [1, 2], [2, 1], [3, 0]], ['O', 'O', 'O', 'O'], 'O'),
    ([[0, 3], [1, 2], [2, 1], [3, 0]], ['O', 'O', 'X', 'O'], None),
    ([[2, 4], [3, 4], [4, 4]], ['O', 'O', 'O'], None),
    ([[1, 4], [2, 4], [3, 4], [4, 4]], ['O', 'O', 'O', 'O'], 'O'),
    ([[1, 4], [2, 4], [3, 4], [4, 4]], ['O', 'O', 'X', 'O'], None),
    ([[1, 2], [2, 2], [3, 2]], ['X', 'X', 'X'], None),
    ([[1, 2], [2, 2], [3, 2], [4, 2]], ['X', 'X', 'X', 'X'], 'X'),
    ([[1, 2], [2, 2], [3, 2], [4, 2]], ['O', 'X', 'X', 'X'], None),
    ([], 'X', None),
])
def test_get_winning_player(fields: list[Field], players: list[str], winner: str) -> None:
    board = FourInRowBoard(6)
    for i, field in enumerate(fields):
        board.update_board(field, players[i])
    assert board.get_winning_player() == winner

@pytest.mark.parametrize('board_size, max_in_row, fields, players , winner', [
    (4, 3, [[0, 0], [0, 3], [1, 0], [1, 1], [2, 2], [3, 3]], ['O', 'O', 'O', 'X', 'X', 'X'], 'X'),
])
def test_edge_cases(board_size:int, max_in_row:int, fields: list[Field], players: list[str], winner: str) -> None:
    board = FourInRowBoard(board_size, max_in_row)
    for i, field in enumerate(fields):
        board.update_board(field, players[i])
    board.print()
    assert board.get_winning_player() == winner