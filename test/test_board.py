from board import Board

def test_get_valid_move_positions():
    board = Board(board_size=3, empty_value='_')
    valid_positions = board.get_valid_move_positions()
    assert len(valid_positions) == 9

