from tictacrow.board import Board, Field


class FourInRowBoard(Board):
    def __init__(self, board_size: int, max_in_row: int = 4) -> None:
        super().__init__(board_size, empty_value=' ')
        self.max_in_row = max_in_row
        self.play_history = []

    def update_board(self, field: Field, value: str, record_history: bool = True, *args, **kwargs) -> 'Board':
        self.board[field[0]][field[1]] = value
        if record_history:
            self.play_history.append(field)
        return self

    def get_winning_player(self) -> str | None:
        if len(self.play_history) == self.board_size * self.board_size:
            return '-'
        for occupied_field in self.play_history:
            if self.is_winner(occupied_field):
                return self.board[occupied_field[0]][occupied_field[1]]
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
                        # print(                          f'current_row: {current_row}, current_column: {current_column} symbol_count: {symbol_count}')
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
