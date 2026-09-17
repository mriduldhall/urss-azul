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
        child_state.apply_deterministic_move(move)

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
class MonteCarloTreeSearchReuseAgent:
    def __init__(self, game, simulations=1000, exploration_constant=sqrt(2), rng=None, chance_policy=None, rollout_policy=None):
        if simulations <= 0:
            raise ValueError("Number of simulations must be greater than 0.")
        self.game = game
        self.rng = rng if rng is not None else Random()
        self.root = StateNode(self.game.clone(), None, None)
        self.simulations = simulations
        self.exploration_constant = exploration_constant
        self.chance_policy = chance_policy
        self.rollout_policy = rollout_policy
        self.selected_node = None

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
            if current_node.state.check_end() or current_node.state.chance_node_required():
                return current_node

            legal_moves = current_node.state.get_legal_actions()
            if len(current_node.children) < len(legal_moves):
                return current_node.expand_node(legal_moves, self.rng)

            current_node = self.select_child(current_node)

    def run_simulation(self, state):
        cloned_state = state.clone()
        first_chance_node = True
        while not cloned_state.check_end():
            if cloned_state.chance_node_required():
                if self.chance_policy is None:
                    raise ValueError("Chance policy required to simulate game with chance nodes.")
                if first_chance_node:
                    cloned_state = self.chance_policy.sample_outcome(cloned_state)
                    first_chance_node = False
                cloned_state.resolve_chance()

            if self.rollout_policy is None:
                move = self.rng.choice(cloned_state.get_legal_actions())
            else:
                move = self.rollout_policy.choose_move(cloned_state, cloned_state.get_legal_actions(), self.rng)
            cloned_state.apply_deterministic_move(move)

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

    def find_root(self, game):
        if self.selected_node is not None:
            self.root = self.selected_node
            for child in self.root.children:
                if child.state == game:
                    child.parent = None
                    return child
        return StateNode(game.clone(), None, None)

    def make_move(self):
        self.root = self.find_root(self.game)
        for _ in range(self.simulations):
            node = self.find_node()
            victory = self.run_simulation(node.state)
            self.backpropagate(node, victory)

        best_child = max(
            self.root.children,
            key=lambda child: (
                child.visits,
                child.reward / child.visits,
            )
        )
        self.selected_node = best_child
        return best_child.move
