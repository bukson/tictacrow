from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Tuple
import numpy as np

Field = list[int] | Tuple[int,int]

class SYMBOL(IntEnum):
    EMPTY = 0
    X = 1
    O = 2
    DRAW = 3


symbol_dict = {
    SYMBOL.EMPTY: ' ',
    SYMBOL.X: 'X',
    SYMBOL.O: 'O',
    SYMBOL.DRAW: '-',
}

class Board(ABC):
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.current_player = SYMBOL.X

    def get_valid_move_positions(self) -> list[Field]:
        empty_positions = np.where(self.board == SYMBOL.EMPTY)
        return list(zip(empty_positions[0], empty_positions[1]))

    def get_occupied_move_positions(self) -> list[Field]:
        empty_positions = np.where(self.board != SYMBOL.EMPTY)
        return list(zip(empty_positions[0], empty_positions[1]))


    def update_board(self, field: Field, symbol: SYMBOL) -> 'Board':
        self.board[tuple(field)] = symbol
        self.update_current_player(symbol)
        return self

    def print(self) -> None:
        print('\n')
        for row in self.board:
            print('|', end='')
            for symbol in row:
                print(f'{symbol_dict[symbol]}|',end='')
            print()
    def is_legal_move(self, field: Field) -> bool:
        for coordinate in field:
            if not (0 <= coordinate < self.board_size):
                return False
        return True

    @abstractmethod
    def get_winning_player(self) -> SYMBOL | None:
        pass

    def update_current_player(self, last_player_symbol: SYMBOL) -> None:
        if last_player_symbol == SYMBOL.X:
            self.current_player = SYMBOL.O
        else:
            self.current_player = SYMBOL.X

