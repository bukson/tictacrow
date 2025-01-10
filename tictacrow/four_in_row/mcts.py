from typing import Optional

from board import Board, Field
import math
import random
from copy import deepcopy, copy


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
        self.untried_moves = set(self.possible_moves)

    def __repr__(self):
        if self.parent is None:
            return f'MTCSNODE(score= {(1 + self.wins) / (1 + self.visits):.2f} ({self.wins}/{self.visits}) player={self.player})'
        else:
            return f'MTCSNODE(score= {(1 + self.wins) / (1 + self.visits):.2f} ({self.wins}/{self.visits}) ucb={self.get_upper_confidence_bound():.8f} player={self.player})'

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

    def add_child(self, move: Field, child: 'MCTSNode'):
        self.children[tuple(move)] = child

    def get_best_child(self):
        return max(self.children.values(), key=lambda child: child.get_upper_confidence_bound())

    def get_most_visited_child(self):
        return max(self.children.values(), key=lambda child: child.visits)

    def get_winning_probability(self) -> float:
        if len(self.children) == 0:
            return 0.0
        else:
            most_visited_child = self.get_most_visited_child()
            return most_visited_child.wins / most_visited_child.visits

    def get_upper_confidence_bound(self, exploration_weight: float = 1.) -> float:
        return (self.wins + self.draws / 2) / self.visits + exploration_weight * math.sqrt(
            math.log(self.parent.visits) / self.visits)


def mcts(root_node: MCTSNode, iterations: int = 4000, random_seed: int = 1) -> Field:
    random.seed(random_seed)
    for _ in range(iterations):
        most_promising_leaf_node = select_most_promising_leaf_node(root_node)
        new_node = expand_node(most_promising_leaf_node)
        winner = simulate_random_game(new_node.state)
        backpropagate_reward(new_node, winner)

    best_move, best_child = max(root_node.children.items(), key=lambda kv: kv[1].visits)
    print(f'Root: {root_node}')
    print(f'Best move: {best_move}')
    return best_move


def select_most_promising_leaf_node(node: MCTSNode) -> MCTSNode:
    while not node.state.get_winning_player() and node.is_fully_expanded():
        node = node.get_best_child()
    return node


def expand_node(node: MCTSNode) -> MCTSNode:
    if node.state.get_winning_player() is None:
        if node.untried_moves:
            random_move = node.untried_moves.pop()
        else:
            valid_moves = node.state.get_valid_move_positions()
            random_move = random.choice(valid_moves)
        if random_move not in node.children:
            next_state = simulate_move(node.state, random_move)
            child_node = MCTSNode(next_state, node.next_player, parent=node)
            node.add_child(random_move, child_node)
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
    valid_moves = state.get_valid_move_positions()
    valid_moves_len = len(valid_moves)
    random.shuffle(valid_moves)
    move_index = 0
    saved_state_current_player = state.current_player
    saved_state_winner = state.winner
    while state.winner is None:
        if move_index == valid_moves_len:
            raise Exception("No valid moves available")
        move = valid_moves[move_index]
        move_index += 1
        state.update_board(move, state.current_player)
    winner = deepcopy(state.winner)
    state.winner = saved_state_winner
    for i in range(0, move_index):
        state.update_board(valid_moves[i], state.empty_value)
    state.current_player = saved_state_current_player
    return winner


def backpropagate_reward(node: MCTSNode, winner: str) -> None:
    while node:
        node.visits += 1
        if winner == node.previous_player:
            node.wins += 1
        if winner == '-':
            node.draws += 1
        node = node.parent
