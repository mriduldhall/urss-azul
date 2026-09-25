from math import exp

class SoftmaxActionSelection:
    def __init__(self, starting_temperature, decay_rate):
        self.starting_temperature = starting_temperature
        self.decay_rate = decay_rate

    def choose_action(self, state, q_table, valid_moves, rng, training_progress):
        temperature = self.starting_temperature * (self.decay_rate ** training_progress)

        q_values = q_table.get_values(state)
        valid_q_values = [q_values[action] for action in valid_moves]
        largest_q_value = max(valid_q_values)

        exp_q_values = [exp((q_values[action] - largest_q_value) / temperature) for action in valid_moves]
        sum_exp_q_values = sum(exp_q_values)
        probabilities = [exp_q_value / sum_exp_q_values for exp_q_value in exp_q_values]

        return rng.choices(valid_moves, weights=probabilities)[0]

    def get_config(self):
        return {
            "name": "softmax",
            "starting_temperature": self.starting_temperature,
            "decay_rate": self.decay_rate,
        }
