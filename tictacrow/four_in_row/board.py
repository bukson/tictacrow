from tictacrow.board import Board, Field


class FourInRowBoard(Board):
    def __init__(self, board_size: int, max_in_row: int = 4) -> None:
        super().__init__(board_size, empty_value=' ')
        self.max_in_row = max_in_row

    def is_move_winning(self, field: Field) -> bool:
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
