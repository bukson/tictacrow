from tictacrow.board import Board, Field, SYMBOL


class FourInRowBoard(Board):
    def __init__(self, board_size: int, max_in_row: int = 4) -> None:
        super().__init__(board_size)
        self.max_in_row = max_in_row

    def get_winning_player(self) -> SYMBOL | None:
        occupied_positions =  self.get_occupied_move_positions()
        if len(occupied_positions) == self.board_size * self.board_size:
            return SYMBOL.DRAW
        for occupied_field in occupied_positions:
            if self.is_winner(occupied_field):
                return self.board[tuple(occupied_field)]
        return None

    def is_winner(self, field: Field) -> bool:
        row, column = field[0], field[1]
        symbol = self.board[row][column]

        def check_direction(delta_row: int, delta_column: int) -> bool:
            symbol_count = 1
            for direction in (-1, 1):
                current_row, current_column = row, column
                while True:
                    current_row += direction * delta_row
                    current_column += direction * delta_column
                    if (self.is_legal_move([current_row, current_column]) and
                            self.board[current_row][current_column] == symbol):
                        symbol_count += 1
                        if symbol_count == self.max_in_row:
                            return True
                    else:
                        break
            return False

        return (
                check_direction(1, 0) or  # Vertical
                check_direction(0, 1) or  # Horizontal
                check_direction(1, 1)  or  # Positive Diagonal \
                check_direction(1, -1)  # Negative Diagonal /
        )
