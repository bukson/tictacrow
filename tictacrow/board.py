from abc import ABC, abstractmethod
from typing import Tuple

Field = Tuple[int, int]


class Board(ABC):
    def __init__(self, board_size: int, empty_value: str = ''):
        self.board_size = board_size
        self.empty_value = empty_value
        self.board = [[empty_value for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'X'
        self.valid_moves = {(x, y) for x in range(self.board_size) for y in range(self.board_size)}
        self.occupied_moves = set()
        self.winner = None

    def get_valid_move_positions(self) -> list[Field]:
        return list(self.valid_moves)

    def get_occupied_move_positions(self) -> list[Field]:
        return list(self.occupied_moves)

    def update_board(self, field: Field, symbol: str) -> 'Board':
        if self.winner is not None:
            raise ValueError('Attempting to update board with winner')
        self.board[field[0]][field[1]] = symbol
        if symbol == self.empty_value:
            self.valid_moves.add(field)
            self.occupied_moves.remove(field)
        else:
            self.occupied_moves.add(field)
            self.valid_moves.remove(field)
            self.update_current_player(symbol)
            if self.is_move_winning(field):
                self.winner = symbol
            else:
                if len(self.valid_moves) == 0:
                    self.winner = '-'
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
    def is_move_winning(self, move: Field) -> str | None:
        pass

    def get_winning_player(self) -> str | None:
        return self.winner

    def update_current_player(self, last_player_symbol: str) -> None:
        if last_player_symbol == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
