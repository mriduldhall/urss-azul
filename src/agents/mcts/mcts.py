from random import Random
from math import log, sqrt

#noinspection DuplicatedCode
class StateNode:
    def __init__(self, state, move, parent):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0

    def expand_node(self, legal_moves, rng):
        tried_moves = [child.move for child in self.children]
        untried_moves = [move for move in legal_moves if move not in tried_moves]
        move = rng.choice(untried_moves)

        child_state = self.state.clone()
        child_state.make_move(move)

        child_node = StateNode(child_state, move, self)
        self.children.append(child_node)
        return child_node

    def calculate_uct(self, exploration_constant, is_maximising):
        if self.visits == 0:
            return float('inf')

        win_rate = self.reward / self.visits
        if not is_maximising:
            win_rate = 1 - win_rate

        exploration_term = exploration_constant * sqrt(log(self.parent.visits) / self.visits)
        return win_rate + exploration_term

    def update(self, win):
        self.visits += 1

        if win:
            self.reward += 1

        if win is None:
            self.reward += 0.5


#noinspection DuplicatedCode
class MonteCarloTreeSearchAgent:
    def __init__(self, game, simulations=1000, exploration_constant=sqrt(2), rng=None):
        self.game = game
        self.rng = rng if rng is not None else Random()
        self.root = StateNode(self.game.clone(), None, None)
        self.simulations = simulations
        self.exploration_constant = exploration_constant

    def select_child(self, current_node):
        best_uct = -float('inf')
        best_child = None
        is_maximising = current_node.state.current_player.value == self.game.current_player.value

        for child in current_node.children:
            uct_value = child.calculate_uct(self.exploration_constant, is_maximising)
            if uct_value > best_uct:
                best_uct = uct_value
                best_child = child

        return best_child

    def find_node(self):
        current_node = self.root
        while True:
            if current_node.state.check_end():
                return current_node

            legal_moves = current_node.state.get_legal_actions()
            if len(current_node.children) < len(legal_moves):
                return current_node.expand_node(legal_moves, self.rng)

            current_node = self.select_child(current_node)

    def run_simulation(self, state):
        cloned_state = state.clone()
        while not cloned_state.check_end():
            move = self.rng.choice(cloned_state.get_legal_actions())
            cloned_state.make_move(move)

        winner = cloned_state.check_victory()
        if winner is None:
            victory = None
        else:
            victory = winner == self.game.current_player.value

        return victory

    @staticmethod
    def backpropagate(node, victory):
        while node is not None:
            node.update(victory)
            node = node.parent

    def make_move(self):
        self.root = StateNode(self.game.clone(), None, None)
        for _ in range(self.simulations):
            node = self.find_node()
            victory = self.run_simulation(node.state)
            self.backpropagate(node, victory)

        best_child = max(self.root.children, key=lambda child: child.visits)
        return best_child.move
