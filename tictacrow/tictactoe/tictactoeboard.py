from board import Board, SYMBOL
import numpy as np

class TicTacToeBoard(Board):
    def __init__(self):
        super().__init__(3)


    def get_winning_player(self) -> SYMBOL | None:
        if len(self.get_valid_move_positions()) == 0:
            return SYMBOL.DRAW

        for symbol in [SYMBOL.X, SYMBOL.O]:

            # for y in range(self.board_size):
            #     if np.all(self.board[y] == symbol.value):
            #         return symbol
            # for x in range(self.board_size):
            #     if np.all(self.board[:,x] == symbol):
            #         return symbol

            for y in range(self.board_size):
                if all(self.board[y][x] == symbol for x in range(self.board_size)):
                    return symbol

            for x in range(self.board_size):
                if all(self.board[y][x] == symbol for y in range(self.board_size)):
                    return symbol

            # positive_diagonal \
            if all([self.board[i][i] == symbol for i in range(self.board_size)]):
                return symbol
            # negative_diagonal /
            if all([self.board[i][(self.board_size -1)- i] == symbol for i in range(self.board_size)]):
                return symbol

        return None

