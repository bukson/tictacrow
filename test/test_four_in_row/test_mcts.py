import pytest

from board import Field, SYMBOL
from four_in_row.board import FourInRowBoard
from four_in_row.mcts import CPUPlayer


@pytest.mark.parametrize('board_size, max_in_row, fields, players , best_move', [
    (3, 3, [[0, 1], [0, 2], [1, 1], [1, 2], [2, 2], ], [SYMBOL.O, SYMBOL.O, SYMBOL.X, SYMBOL.X, SYMBOL.X], [0, 0]),
    (3, 3, [[0, 2], [1, 1], [1, 2], ], [SYMBOL.O, SYMBOL.X, SYMBOL.X], [1, 0]),
    (5, 4, [[1, 4], [2, 2], [2, 3], [3, 1], [3, 2]], [SYMBOL.X, SYMBOL.O, SYMBOL.X, SYMBOL.O, SYMBOL.X], [4, 1]),
])
def test_edge_cases_mcts(board_size: int, max_in_row: int, fields: list[Field], players: list[SYMBOL],
                    best_move: Field) -> None:
    board = FourInRowBoard(board_size, max_in_row)
    for i, field in enumerate(fields):
        board.update_board(field, players[i])
    board.print()
    cpu = CPUPlayer(board, SYMBOL.O, 2000)
    cpu_move = cpu.select_best_move_mcts()
    assert cpu_move == best_move


def test_minimax_mcts_tic_tac_toe() -> None:
    board = FourInRowBoard(3, 3)
    board.print()
    cpu = CPUPlayer(board, SYMBOL.X, 500)
    cpu_move = cpu.select_best_move_minimax_mcts()
    assert cpu_move == [1,1]

@pytest.mark.parametrize('board_size, max_in_row, fields, players , best_move', [
    (3, 3, [[0, 1], [0, 2], [1, 1], [1, 2], [2, 2], ], [SYMBOL.O, SYMBOL.O, SYMBOL.X, SYMBOL.X, SYMBOL.X], [0, 0]),
    (3, 3, [[0, 2], [1, 1], [1, 2], ], [SYMBOL.O, SYMBOL.X, SYMBOL.X], [1, 0]),
    (5, 4, [[1, 4], [2, 2], [2, 3], [3, 1], [3, 2]], [SYMBOL.X, SYMBOL.O, SYMBOL.X, SYMBOL.O, SYMBOL.X], [4, 1]),
])
def test_edge_cases_minimax_mcts(board_size: int, max_in_row: int, fields: list[Field], players: list[SYMBOL],
                    best_move: Field) -> None:
    board = FourInRowBoard(board_size, max_in_row)
    for i, field in enumerate(fields):
        board.update_board(field, players[i])
    board.print()
    cpu = CPUPlayer(board, SYMBOL.O, 200)
    cpu_move = cpu.select_best_move_minimax_mcts()
    assert cpu_move == best_move
