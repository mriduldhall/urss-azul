import json

class QTable:
    def __init__(self, action_count):
        self.q_table = {}
        self.action_count = action_count

    def create_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0] * self.action_count

    def get_values(self, state):
        self.create_state(state)
        return self.q_table[state]

    def get_value(self, state, action):
        self.create_state(state)
        return self.q_table[state][action]

    def update(self, state, action, target, learning_rate):
        self.create_state(state)
        old_value = self.q_table[state][action]
        self.q_table[state][action] = old_value + learning_rate * (target - old_value)
        return self.q_table[state][action]

    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.q_table, file)
