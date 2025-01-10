from copy import deepcopy


from board import Field, Board
from four_in_row.board import FourInRowBoard
from abc import abstractmethod, ABC

from four_in_row.gui import NInRowGui
from four_in_row.mcts import MCTSNode, mcts


class Player(ABC):
    def __init__(self, board: Board, symbol: str, default_elo: int = 1200):
        self.board = board
        self.symbol = symbol
        self.elo = default_elo

    @abstractmethod
    def get_move(self) -> Field:
        pass

    @abstractmethod
    def register_opponent_move(self, move: Field, symbol:str) -> None:
        pass


class HumanPlayer(Player):

    def __init__(self , board: Board, symbol: str, gui: NInRowGui) -> None:
        super().__init__(board, symbol)
        self.gui = gui

    def get_move(self) -> Field:
        move = deepcopy(self.gui.current_move)
        self.gui.current_move = None
        return move

    def register_opponent_move(self, move: Field, symbol:str) -> None:
        pass


class CPUPlayer(Player):
    def __init__(self, board: Board, symbol: str = 'O', iterations: int = 2000,
                 random_seed: int = 0) -> None:
        super().__init__(board, symbol)
        self.board = deepcopy(board)
        self.symbol = symbol
        self.iterations = iterations
        self.mcts_node = MCTSNode(self.board, symbol)
        self.random_seed = random_seed

    def get_move(self) -> Field:
        self.mcts_node = MCTSNode(self.board, self.symbol)
        best_move = mcts(self.mcts_node, iterations=self.iterations, random_seed=self.random_seed)
        for move, child in sorted(self.mcts_node.children.items(), key=lambda kv: kv[1].visits, reverse=True)[:4]:
            print(move, child)
        self.board.update_board(best_move, self.symbol)

        self.board.print()
        return best_move

    def register_opponent_move(self, opponent_move: Field, opponent_symbol:str) -> None:
        self.board.update_board(opponent_move, opponent_symbol)
        if len(self.mcts_node.children) == 0:
            return
        else:
            # self.mcts_node = self.mcts_node.children[best_move]
            # self.mcts_node = self.mcts_node.children[opponent_move]
            print(f'{self.symbol}: visited this position {self.mcts_node.visits} times with win rate {self.mcts_node.wins / self.mcts_node.visits}')



class NinRowGame:
    def __init__(self, board_size: int = 11, in_row: int = 5, iterations = 60000, random_seed:int=0):
        self.board_size = board_size
        self.board = FourInRowBoard(board_size, in_row)
        self.in_row = in_row
        self.gui = NInRowGui(board_size=11, in_row=5)
        self.players = [HumanPlayer(self.board, 'X', self.gui), CPUPlayer(self.board, 'O', iterations, random_seed)]
        self.players = [CPUPlayer(self.board, 'X', iterations, random_seed=1), CPUPlayer(self.board, 'O', iterations, random_seed)]
        # self.players = [HumanPlayer(self.board, 'X', self.gui), HumanPlayer(self.board, 'O', self.gui)]
        self.current_player = 0

    def is_ending(self) -> bool:
        return self.board.get_winning_player() is not None

    def game_loop(self):
        if self.is_ending():
            winner = self.board.get_winning_player()
            self.gui.show_victory_screen(winner)
            self.board = FourInRowBoard(self.board_size, self.in_row)
            self.current_player = 0
            self.gui.reset_game()

        player = self.players[self.current_player]
        if isinstance(player, HumanPlayer):
            if self.gui.current_move is not None:
                move = player.get_move()
                self.process_move(move)
        else:
            move = player.get_move()
            self.process_move(move)

        self.gui.root.after(100, self.game_loop)  # Schedule the next iteration

    def process_move(self, move: Field):
        self.board.update_board(move, self.players[self.current_player].symbol)
        self.gui.buttons[move[0]][move[1]].config(text=self.players[self.current_player].symbol)
        next_player = (self.current_player + 1) % 2
        self.players[next_player].register_opponent_move(move, self.players[self.current_player].symbol)
        self.current_player = next_player

    def start(self):
        self.gui.draw_board()
        self.gui.root.after(100, self.game_loop)  # Start the game loop
        self.gui.start()



if __name__ == "__main__":
    application = NinRowGame(board_size=11, in_row=5, random_seed=1526)
    application.start()
