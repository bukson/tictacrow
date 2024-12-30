from tictacrow.board import Field, Board
import random

def minimax(board: Board, depth:int, is_maximizing: bool) -> float:
    player = 'X' if is_maximizing else 'O'
    if (winning_player := board.get_winning_player()) is not None:
        if winning_player == '-':
            return 0.0
        elif winning_player == 'X':
            return 1.0
        else:
            return -1.0
    valid_moves = board.get_valid_move_positions()
    if depth == 0:
        return random.uniform(-0.5,0.5)
    if is_maximizing:
        value = -2
        for field in valid_moves:
            board.update_board(field, player, record_history=False)
            value = max(value, minimax(board, depth-1, not is_maximizing))
            board.update_board(field, board.empty_value, record_history=False)
    else:
        value = 2
        for field in valid_moves:
            board.update_board(field, player, record_history=False)
            value = min(value, minimax(board, depth-1, not is_maximizing))
            board.update_board(field, board.empty_value, record_history=False)
    return value


class CPUPlayer:
    def __init__(self, board: Board, player: str = 'O') -> None:
        self.board = board
        self.player = player
        self.depth = 5
    def select_best_move_minimax(self) -> Field:
        is_maximizing = True if self.player == 'X' else False
        current_best_move = None
        current_best_value = -2 if is_maximizing else 2

        for field in self.board.get_valid_move_positions():
            self.board.update_board(field, self.player, record_history=False)
            move_value = minimax(self.board, self.depth, not is_maximizing)
            self.board.update_board(field, self.board.empty_value, record_history=False)
            if is_maximizing and move_value > current_best_value:
                current_best_move = field
                current_best_value = move_value
            elif not is_maximizing and move_value < current_best_value:
                current_best_move = field
                current_best_value = move_value
            # print(field, move_value)
        # print(f'Current best value: {current_best_value}')
        # print(f'Current best move: {current_best_move}')
        # print(f'Current is_maximizing: {is_maximizing}')
        return current_best_move
