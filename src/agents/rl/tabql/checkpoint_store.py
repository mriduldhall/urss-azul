import json
from agents.rl.tabql.config import TabQLConfig
from agents.rl.tabql.checkpoint import TabQLCheckpoint

class TabQLCheckpointStore:
    @staticmethod
    def save(filename, checkpoint):
        data = checkpoint.to_data()
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        config = TabQLConfig.from_data(data["config"])
        completed_episodes = data["completed_episodes"]
        next_learner_starts = data["next_learner_starts"]
        rng_state = self.load_rng(data["rng_state"])
        q_table = data["q_table"]
        return TabQLCheckpoint(config, completed_episodes, next_learner_starts, rng_state, q_table)

    def load_rng(self, value):
        if isinstance(value, list):
            return tuple(self.load_rng(item) for item in value)

        if isinstance(value, dict):
            return {key: self.load_rng(val) for key, val in value.items()}

        return value
