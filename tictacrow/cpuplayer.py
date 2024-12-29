from tictactoe import TicTacToeBoard, Field


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


class CPUPlayer:
    def __init__(self, board: TicTacToeBoard, player: str = 'O') -> None:
        self.board = board
        self.player = player

    def select_best_move_minimax(self) -> Field:
        is_maximizing = True if self.player == 'X' else False
        current_best_move = None
        current_best_value = -1 if is_maximizing else 1

        for field in self.board.get_valid_move_positions():
            self.board.update_board(field, self.player)
            move_value = minimax(self.board, not is_maximizing)
            self.board.update_board(field, self.board.empty_value)
            if is_maximizing and move_value > current_best_value:
                current_best_move = field
                current_best_value = move_value
            elif not is_maximizing and move_value < current_best_value:
                current_best_move = field
                current_best_value = move_value
            print(field, move_value)
        print(f'Current best value: {current_best_value}')
        print(f'Current best move: {current_best_move}')
        print(f'Current is_maximizing: {is_maximizing}')
        return current_best_move
