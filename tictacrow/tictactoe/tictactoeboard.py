from board import Board


class TicTacToeBoard(Board):
    def __init__(self):
        super().__init__(3, ' ')


    def get_winning_player(self) -> str | None:
        if len(self.get_valid_move_positions()) == 0:
            return '-'
        for symbol in ['X', 'O']:

            for y in range(self.board_size):
                if all(self.board[y][x] == symbol for x in range(self.board_size)):
                    return symbol

            for x in range(self.board_size):
                if all(self.board[y][x] == symbol for y in range(self.board_size)):
                    return symbol

            # positive_diagonal
            if all([self.board[i][i] == symbol for i in range(self.board_size)]):
                return symbol
            # negative_diagonal
            if all([self.board[i][(self.board_size -1)- i] == symbol for i in range(self.board_size)]):
                return symbol

        return None

