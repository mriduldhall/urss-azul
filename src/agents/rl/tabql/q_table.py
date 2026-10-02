import json

class QTable:
    def __init__(self, action_count, action_mapping):
        self.q_table = {}
        self.action_count = action_count
        self.action_mapping = action_mapping

    def create_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0] * self.action_count

    def get_values(self, state):
        self.create_state(state)
        return self.q_table[state]

    def get_value(self, state, action):
        self.create_state(state)
        return self.q_table[state][self.action_mapping.get_mapping(action)]

    def update(self, state, action, target, learning_rate):
        self.create_state(state)
        mapped_action = self.action_mapping.get_mapping(action)
        old_value = self.q_table[state][mapped_action]
        self.q_table[state][mapped_action] = old_value + learning_rate * (target - old_value)
        return self.q_table[state][mapped_action]

    def to_data(self):
        return {
            "action_count": self.action_count,
            "q_table": self.q_table,
            "action_mapping": self.action_mapping.get_config(),
        }

    @staticmethod
    def from_data(data, action_mapping):
        if data["action_mapping"] != action_mapping.get_config():
            raise ValueError("Action mapping configuration does not match.")
        q_table_instance = QTable(data["action_count"], action_mapping)
        q_table_instance.q_table = data["q_table"]
        return q_table_instance

    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_data(), file)

    @staticmethod
    def load(filename, action_mapping):
        with open(filename, 'r') as file:
            data = json.load(file)

        action_count = data["action_count"]
        if action_count != len(next(iter(data["q_table"].values()))):
            raise ValueError("Action count does not match.")

        if data["action_mapping"] != action_mapping.get_config():
            raise ValueError("Action mapping configuration does not match.")

        q_table_instance = QTable(action_count, action_mapping)
        q_table_instance.q_table = data["q_table"]
        
        return q_table_instance
