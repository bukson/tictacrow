from typing import Optional

from board import Board, Field
import math
import random
from copy import deepcopy


class MCTSNode:
    def __init__(self, state: Board, player: str, parent: Optional['MCTSNode'] = None):
        self.state = state
        self.parent = parent
        self.player = player
        self.children = {}
        self.visits = 0
        self.wins = 0
        self.draws = 0
        self.possible_moves = self.state.get_valid_move_positions()

    def __repr__(self):
        return f'MTCSNODE(score= {self.wins/self.visits:.2f} ({self.wins}/{self.visits}) player={self.player})'

    @property
    def previous_player(self) -> str:
        if self.player == 'X':
            return 'O'
        else:
            return 'X'

    @property
    def next_player(self) -> str:
        return self.previous_player

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





def mcts(root_node: MCTSNode, iterations: int = 4000, random_seed:int=1) -> Field:
    random.seed(random_seed)
    for _ in range(iterations):
        most_promising_leaf_node = select_most_promising_leaf_node(root_node)
        new_node = expand_node(most_promising_leaf_node)
        winner = simulate_random_game(new_node.state)
        backpropagate_reward(new_node, winner)

    best_move, best_child = max(root_node.children.items(), key=lambda kv: kv[1].visits)
    print(f'Root: {root_node}')
    print(f'Best move: {best_move}')
    return list(best_move)


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
        if random_move not in node.children:
            next_state = simulate_move(node.state, list(random_move))
            child_node = MCTSNode(next_state, node.next_player, parent=node)
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
    moves_to_unroll = []
    while (winner := state.get_winning_player()) is None:
        valid_moves = state.get_valid_move_positions()
        if len(valid_moves) == 0:
            raise Exception("No valid moves available")
        move = random.choice(state.get_valid_move_positions())
        moves_to_unroll.append(move)
        state.update_board(move, state.current_player)
    for move in moves_to_unroll:
        state.update_board(move, state.empty_value)
    return winner


def backpropagate_reward(node: MCTSNode, winner: str) -> None:
    while node:
        node.visits += 1
        if winner == node.previous_player:
            node.wins += 1
        if winner == '-':
            node.draws += 1
        node = node.parent


class CPUPlayer:
    def __init__(self, board: Board, player: str = 'O', iterations: int = 2000, random_seed:int=0) -> None:
        self.board = board
        self.player = player
        self.iterations = iterations
        self.mcts_node = MCTSNode(deepcopy(self.board), player)
        self.random_seed = random_seed

    def select_best_move_mcts(self) -> Field:
        mcts_node = MCTSNode(deepcopy(self.board), self.player)
        best_move = mcts(mcts_node, iterations=self.iterations, random_seed=self.random_seed)
        for move, child in sorted(mcts_node.children.items(), key=lambda kv: kv[1].visits, reverse=True):
            print(move, child)
        return best_move

