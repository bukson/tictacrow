import pytest

from four_in_row.game import CPUPlayer
from tictacrow.board import Field
from four_in_row.board import FourInRowBoard


@pytest.mark.parametrize('board_size, max_in_row, fields, players , best_move', [
    # (3, 3, [0, 1), (0, 2), (1, 1), (1, 2), (2, 2), ], ('O', 'O', 'X', 'X', 'X'), (()0, 0)),
    # (3, 3, [(0, 2), (1, 1), (1, 2), ], ('O', 'X', 'X'), (1, 0)),
    # (5, 4, [(1, 4), (2, 2), (2, 3), (3, 1), (3, 2)], ('X', 'O', 'X', 'O', 'X'), (4, 1)),
    (11, 5, [(1, 4), (2, 2), (3, 6), (7, 7), (7, 8), (7, 9), (7, 10)], ('O', 'O', 'O', 'X', 'X', 'X', 'X'), (7, 6)),

])
def test_edge_cases_mcts(board_size: int, max_in_row: int, fields: list[Field], players: list[str],
                         best_move: Field) -> None:
    board = FourInRowBoard(board_size, max_in_row)
    for i, field in enumerate(fields):
        board.update_board(field, players[i])
    board.print()
    cpu = CPUPlayer(board, 'O', 10000)
    cpu_move = cpu.get_move()
    assert cpu_move == best_move


@pytest.mark.parametrize('board_size, max_in_row, fields, players , expected_maximal_winning_probability', [
    # (3, 3, [0, 1), (0, 2), (1, 1), (1, 2), (2, 2), ], ('O', 'O', 'X', 'X', 'X'), (()0, 0)),
    # (3, 3, [(0, 2), (1, 1), (1, 2), ], ('O', 'X', 'X'), (1, 0)),
    # (5, 4, [(1, 4), (2, 2), (2, 3), (3, 1), (3, 2)], ('X', 'O', 'X', 'O', 'X'), (4, 1)),
    (11, 5, [(1, 4), (2, 4), (2, 2), (3, 6), (7, 6), (7, 7), (7, 8), (7, 9)], ('O', 'O', 'O', 'O', 'X', 'X', 'X', 'X'),
     0.5),

])
def test_board_value_mcts(board_size: int, max_in_row: int, fields: list[Field], players: list[str],
                          expected_maximal_winning_probability: float) -> None:
    board = FourInRowBoard(board_size, max_in_row)
    for i, field in enumerate(fields):
        board.update_board(field, players[i])
    board.print()
    cpu = CPUPlayer(board, 'O', 10000)
    cpu_move = cpu.get_move()
    winning_probability = cpu.mcts_node.get_winning_probability()
    assert winning_probability < expected_maximal_winning_probability
