from tictactoe import TicTacToeBoard


def minimax(board: TicTacToeBoard, is_maximizing: bool) -> int:
    player = 'X' if is_maximizing else 'O'
    if (winning_player := board.get_winning_player()) is not None:
        if winning_player == '-':
            return 0
        elif winning_player == 'X':
            return 1
        else:
            return -1
    if is_maximizing:
        value = -1
        for field in board.get_valid_move_positions():
            board.update_board(field, player)
            value = max(value, minimax(board, not is_maximizing))
            board.update_board(field, board.empty_value)
    else:
        value = 1
        for field in board.get_valid_move_positions():
            board.update_board(field, player)
            value = min(value, minimax(board, not is_maximizing))
            board.update_board(field, board.empty_value)
    return value