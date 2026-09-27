class TabQLCheckpoint:
    def __init__(self, config, completed_episodes, next_learner_starts, rng_state, q_table):
        self.config = config
        self.completed_episodes = completed_episodes
        self.next_learner_starts = next_learner_starts
        self.rng_state = rng_state
        self.q_table = q_table

    def to_data(self):
        return {
            "config": self.config,
            "completed_episodes": self.completed_episodes,
            "next_learner_starts": self.next_learner_starts,
            "rng_state": self.rng_state,
            "q_table": self.q_table,
        }
