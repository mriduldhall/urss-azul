from random import Random
from agents.rl.tabql.q_table import QTable

class TabqlAgent:
    def __init__(self, game, filename, state_encoder, rng=None):
        self.game = game
        self.q_table = QTable.load(filename)
        self.state_encoder = state_encoder
        self.rng = rng if rng is not None else Random()

    def make_move(self):
        valid_actions = self.game.get_legal_actions()
        state = self.state_encoder.encode(self.game)
        q_values = self.q_table.get_values(state)
        max_q_value = max(q_values[action] for action in valid_actions)
        best_actions = [action for action in valid_actions if q_values[action] == max_q_value]
        return self.rng.choice(best_actions)
