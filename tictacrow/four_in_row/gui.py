import tkinter as tk
from tkinter import messagebox

from four_in_row.board import FourInRowBoard


class NInRowGui:
    def __init__(self, board_size:int = 25, in_row: int = 3):
        self.root = tk.Tk()
        self.root.title("4 in Row")
        self.mutex = False
        self.board_size_pixels = 600
        self.board_size = board_size
        self.board = FourInRowBoard(board_size, in_row)
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_move = None

    def draw_board(self):

        # Add column numbers at the top
        for column in range(self.board_size):
            label = tk.Label(self.root, text=str(column), font=("Arial", 14), width=5)
            label.grid(row=0, column=column + 1)  # Offset by 1 for row numbers on the left

        # Add row numbers on the left
        for row in range(self.board_size):
            label = tk.Label(self.root, text=str(row), font=("Arial", 14), height=2)
            label.grid(row=row + 1, column=0)  # Offset by 1 for column numbers at the top

            # Draw the board
            for row in range(self.board_size):
                for column in range(self.board_size):
                    button = tk.Button(self.root, text="", font=("Arial", 24), height=2, width=5,
                                       command=lambda r=row, c=column: self.make_move(r, c))
                    button.grid(row=row + 1, column=column + 1)  # Offset by 1 for labels
                    self.buttons[row][column] = button

    def make_move(self, row: int, col: int):
        if self.current_move is None and self.buttons[row][col]["text"] == "":
            self.current_move = (row, col)

    def show_victory_screen(self, winning_player:str) -> None:
        if winning_player == '-':
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            messagebox.showinfo("Game Over", f"Player {winning_player} wins!")

    def start(self) -> None:
        self.root.mainloop()

    def reset_game(self) -> None:
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].config(text="")
        self.current_move = None


