from tictacrow.board import Board, Field



class FourInRowBoard(Board):
    def __init__(self, board_size: int, max_in_row: int = 4) -> None:
        super().__init__(board_size, empty_value=' ')
        self.max_in_row = max_in_row

    def is_move_winning(self, field: Field) -> bool:
        row, column = field[0], field[1]
        symbol = self.board[row][column]

        def count_in_direction(delta_row: int, delta_column: int) -> int:
            count = 0
            current_row, current_column = row + delta_row, column + delta_column
            while (
                0 <= current_row < self.board_size and
                0 <= current_column < self.board_size and
                self.board[current_row][current_column] == symbol
            ):
                count += 1
                current_row += delta_row
                current_column += delta_column
            return count

        # Check all directions: vertical, horizontal, and two diagonals
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for delta_row, delta_column in directions:
            # Count both forward and backward in this direction
            total_count = 1 + count_in_direction(delta_row, delta_column) + count_in_direction(-delta_row, -delta_column)
            if total_count >= self.max_in_row:
                return True

        return False