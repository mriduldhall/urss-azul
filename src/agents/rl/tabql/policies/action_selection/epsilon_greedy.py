class EpsilonGreedyActionSelection:
    def __init__(self, epsilon):
        if epsilon < 0 or epsilon > 1:
            raise ValueError("Epsilon must be between 0 and 1.")
        self.epsilon = epsilon

    def choose_action(self, state, q_table, valid_moves, rng, training_progress):
        if rng.random() < self.epsilon:
            return rng.choice(valid_moves)

        q_values = q_table.get_values(state)
        max_q_value = max(q_values[action] for action in valid_moves)
        best_actions = [action for action in valid_moves if q_values[action] == max_q_value]
        return rng.choice(best_actions)

    def get_config(self):
        return {
            "name": "epsilon-greedy",
            "epsilon": self.epsilon,
        }
