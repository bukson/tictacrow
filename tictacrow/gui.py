import tkinter as tk
from tkinter import messagebox

from cpuplayer import CPUPlayer
from tictactoe import TicTacToeBoard


class TitTacToeGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.board_size = 600
        # self.canvas = tk.Canvas(self.root, width=self.board_size, height=self.board_size)
        self.board = TicTacToeBoard()
        self.current_player = 'X'
        self.cpu = CPUPlayer(self.board, player='O')

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for column in range(3):
                button = tk.Button(self.root, text="", font=("Arial", 24), height=5, width=10,
                                   command=lambda r=row, c=column: self.make_move(r, c))
                button.grid(row=row, column=column)
                self.buttons[row][column] = button

    def make_move(self, row: int, col: int, is_player_move:bool=True) -> None:
        if self.board.board[row][col] != self.board.empty_value:
            return

        self.board.update_board([row, col], self.current_player)
        self.buttons[row][col].config(text=self.current_player)
        self.board.print()

        if (winning_player := self.board.get_winning_player()) is not None:
            if winning_player == '-':
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            return
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            if is_player_move:
                cpu_move = self.cpu.select_best_move_minimax()
                self.make_move(cpu_move[0], cpu_move[1], is_player_move=False)


    def start(self) -> None:
        self.root.mainloop()

    def reset_game(self) -> None:
        self.current_player = 'X'
        self.board = TicTacToeBoard()
        self.cpu = CPUPlayer(self.board, player='O')
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")


if __name__ == "__main__":
    application = TitTacToeGui()
    application.start()
