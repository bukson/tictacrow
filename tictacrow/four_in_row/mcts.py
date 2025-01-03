from typing import Optional

from board import Board, Field, SYMBOL
import math
import random
from copy import deepcopy


class MCTSNode:
    def __init__(self, state: Board, parent: Optional['MCTSNode'] = None):
        self.state = state
        self.parent = parent
        self.player = state.current_player
        self.children = {}
        self.visits = 0
        self.wins = 0
        self.draws = 0
        self.possible_moves = self.state.get_valid_move_positions()

    def __repr__(self):
        return f'MTCSNODE(score= {self.wins / self.visits:.2f}, {self.wins}/{self.visits}, draws={self.draws}, current_player={self.player})'

    @property
    def previous_player(self) -> SYMBOL:
        if self.player == SYMBOL.X:
            return SYMBOL.O
        else:
            return SYMBOL.X

    def is_fully_expanded(self):
        return len(self.children) == len(self.possible_moves)

    def get_best_child(self):
        return max(self.children.values(), key=lambda child: child.get_upper_confidence_bound())

    def get_upper_confidence_bound(self, exploration_weight: float = 1.) -> float:
        if self.visits == 0:
            return float("inf")
        elif self.parent is None:
            print('Warning. trying to calculate upper confidence bound for root node!')
            return 1.0
        else:
            return (self.wins + self.draws / 2) / self.visits + exploration_weight * math.sqrt(
                math.log(self.parent.visits) / self.visits)


def mcts(root_node: MCTSNode, iterations: int = 4000, random_seed: int = 0) -> Field:
    random.seed(random_seed)
    for _ in range(iterations):
        most_promising_leaf_node = select_most_promising_leaf_node(root_node)
        new_node = expand_node(most_promising_leaf_node)
        winner = simulate_random_game(new_node.state)
        backpropagate_reward(new_node, winner)

    best_move, best_child = max(root_node.children.items(), key=lambda kv: kv[1].visits)
    print(f'Root: {root_node}')
    print(f'Best move: {[int(best_move[0]), int(best_move[1])]} {best_child}')
    return [int(best_move[0]), int(best_move[1])]


def select_most_promising_leaf_node(node: MCTSNode) -> MCTSNode:
    while node.state.get_winning_player() is None:
        if node.is_fully_expanded():
            return node.get_best_child()
        else:
            return node


def expand_node(node: MCTSNode) -> MCTSNode:
    if node.state.get_winning_player() is None:
        valid_moves = node.state.get_valid_move_positions()
        random_move = tuple(random.choice(valid_moves))
        if random_move == (0, 0) and node.player == SYMBOL.O:
            pass
        if random_move not in node.children:
            next_state = simulate_move(node.state, list(random_move))
            child_node = MCTSNode(next_state, parent=node)
            node.children[tuple(random_move)] = child_node
            return child_node
        else:
            return node.children[random_move]
    else:
        return node


def simulate_move(state: Board, move: Field) -> Board:
    new_state = deepcopy(state)
    new_state.update_board(move, new_state.current_player)
    return new_state


def simulate_random_game(state: Board) -> str:
    current_state = deepcopy(state)
    while (winner := current_state.get_winning_player()) is None:
        valid_moves = current_state.get_valid_move_positions()
        if len(valid_moves) == 0:
            raise Exception("No valid moves available")
        move = random.choice(current_state.get_valid_move_positions())
        current_state.update_board(move, current_state.current_player)
    return winner


def backpropagate_reward(node: MCTSNode, winner: str) -> None:
    while node:
        node.visits += 1
        if winner == node.previous_player:
            node.wins += 1
        if winner == SYMBOL.DRAW:
            node.draws += 1
        node = node.parent


class CPUPlayer:
    def __init__(self, board: Board, player: SYMBOL = SYMBOL.O, iterations: int = 2000, random_seed: int = 0) -> None:
        self.board = board
        self.player = player
        self.iterations = iterations
        self.mcts_node = MCTSNode(deepcopy(self.board))
        self.random_seed = random_seed

    def select_best_move_mcts(self) -> Field:
        mcts_node = MCTSNode(deepcopy(self.board))
        best_move = mcts(mcts_node, iterations=self.iterations, random_seed=self.random_seed)
        for move, child in sorted(mcts_node.children.items(), key=lambda kv: kv[1].visits, reverse=True):
            print(f'Move: {[int(move[0]), int(move[1])]}, {child}')
        return best_move

    def select_best_move_minimax_mcts(self, depth: int = 1) -> Field:
        is_maximizing = True if self.player == SYMBOL.X else False
        current_best_move = None
        current_best_value = -1 if is_maximizing else 1

        for field in self.board.get_valid_move_positions():
            field = [int(field[0]), int(field[1])]
            self.board.update_board(field, self.player)
            move_value = minimax_mcts(self.board, depth, self.iterations, not is_maximizing)
            self.board.update_board(field, SYMBOL.EMPTY)
            if is_maximizing and move_value > current_best_value:
                current_best_move = field
                current_best_value = move_value
            elif not is_maximizing and move_value < current_best_value:
                current_best_move = field
                current_best_value = move_value
            print(field, move_value)
        print(f'Current best value: {current_best_value}')
        print(f'Current best move: {current_best_move}')
        print(f'Current is_maximizing: {is_maximizing}')
        return current_best_move


def minimax_mcts(board: Board, depth: int, iterations: int, is_maximizing: bool) -> float:
    player = SYMBOL.X if is_maximizing else SYMBOL.O
    if (winning_player := board.get_winning_player()) is not None:
        if winning_player == '-':
            return 0.5
        elif winning_player == SYMBOL.X:
            return 1.
        else:
            return 0.
    if (depth == 0):
        mcts_node = MCTSNode(deepcopy(board))
        best_move = mcts(mcts_node, iterations=iterations)
        return mcts_node.wins / mcts_node.visits
    if is_maximizing:
        value = -1
        for field in board.get_valid_move_positions():
            board.update_board(field, player)
            value = max(value, minimax_mcts(board, depth - 1, iterations, not is_maximizing))
            board.update_board(field, SYMBOL.EMPTY)
    else:
        value = 1
        for field in board.get_valid_move_positions():
            board.update_board(field, player)
            value = min(value, minimax_mcts(board, depth - 1, iterations, not is_maximizing))
            board.update_board(field, SYMBOL.EMPTY)
    return value
