from random import Random
from agents.rl.tabql.q_table import QTable

class TabqlAgent:
    def __init__(self, game, filename, state_encoder, action_mapping, rng=None):
        self.game = game
        self.q_table = QTable.load(filename, action_mapping)
        self.state_encoder = state_encoder
        self.action_mapping = action_mapping
        self.rng = rng if rng is not None else Random()

    def make_move(self):
        valid_actions = self.game.get_legal_actions()
        state = self.state_encoder.encode(self.game)
        q_values = self.q_table.get_values(state)
        max_q_value = max(q_values[self.action_mapping.get_mapping(action)] for action in valid_actions)
        best_actions = [action for action in valid_actions if q_values[self.action_mapping.get_mapping(action)] == max_q_value]
        return self.rng.choice(best_actions)
