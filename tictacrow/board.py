from abc import ABC, abstractmethod
Field = list[int]


class Board(ABC):
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

    def get_occupied_move_positions(self) -> list[Field]:
        positions = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] != self.empty_value:
                    positions.append([y, x])
        return positions

    def update_board(self, field: Field, symbol: str) -> 'Board':
        self.board[field[0]][field[1]] = symbol
        self.update_current_player(symbol)
        return self

    def print(self) -> None:
        print('\n')
        for row in self.board:
            print(row)

    def is_legal_move(self, field: Field) -> bool:
        for coordinate in field:
            if not (0 <= coordinate < self.board_size):
                return False
        return True

    @abstractmethod
    def get_winning_player(self) -> str | None:
        pass

    def update_current_player(self, last_player_symbol: str) -> None:
        if last_player_symbol == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

