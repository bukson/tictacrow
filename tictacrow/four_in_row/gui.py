import tkinter as tk
from tkinter import messagebox

from tictacrow.board import SYMBOL, symbol_dict
from four_in_row.mcts import CPUPlayer
from four_in_row.board import FourInRowBoard


class FourInRowGui:
    def __init__(self, board_size:int = 25, in_row: int = 3, *args, **kwargs):
        self.root = tk.Tk()
        self.root.title("4 in Row")
        self.board_size_pixels = 600
        self.board_size = board_size
        self.board = FourInRowBoard(board_size, in_row)
        self.current_player = SYMBOL.X
        self.cpu = CPUPlayer(self.board, player=SYMBOL.O, iterations=kwargs.get('iterations', 2000))

        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(self.board_size):
            for column in range(self.board_size):
                button = tk.Button(self.root, text="", font=("Arial", 24), height=2, width=5,
                                   command=lambda r=row, c=column: self.make_move(r, c))
                button.grid(row=row, column=column)
                self.buttons[row][column] = button

    def make_move(self, row: int, col: int, is_player_move:bool=True) -> None:
        if self.board.board[row][col] != SYMBOL.EMPTY:
            return

        self.board.update_board([row, col], self.current_player)
        self.buttons[row][col].config(text=symbol_dict[self.current_player])
        self.board.print()
        if (winning_player := self.board.get_winning_player()) is not None:
            if winning_player == SYMBOL.DRAW:
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            return
        else:
            self.current_player = SYMBOL.O if self.current_player == SYMBOL.X else SYMBOL.X
            if is_player_move:
                # cpu_move = self.cpu.select_best_move_mcts()
                cpu_move = self.cpu.select_best_move_minimax_mcts()
                self.make_move(cpu_move[0], cpu_move[1], is_player_move=False)


    def start(self) -> None:
        self.root.mainloop()

    def reset_game(self) -> None:
        self.current_player = 'X'
        self.board = FourInRowBoard(self.board_size)
        self.cpu = CPUPlayer(self.board, player=SYMBOL.O, iterations=self.cpu.iterations)
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].config(text="")


if __name__ == "__main__":
    application = FourInRowGui(board_size=11, in_row=5, iterations=200)
    application.start()
