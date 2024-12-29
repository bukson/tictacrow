from copy import deepcopy

Field = list[int]


class Board:
    def __init__(self, board_size: int, empty_value: str = ''):
        self.board_size = board_size
        self.empty_value = empty_value
        self.board = [[empty_value for _ in range(self.board_size)] for _ in range(self.board_size)]

    def get_valid_move_positions(self) -> list[Field]:
        positions = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] == self.empty_value:
                    positions.append([y, x])
        return positions

    def update_board(self, field: Field, value: str) -> 'Board':
        self.board[field[0]][field[1]] = value
        return self

    def print(self) -> None:
        for row in self.board:
            print(row)

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

