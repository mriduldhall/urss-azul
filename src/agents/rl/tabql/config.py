class TabQLConfig:
    def __init__(self, environment, opponent_agent, state_encoder, action_encoder, reward_policy, exploration_policy, self_play, learning_rate, discount_factor):
        self.environment = environment
        self.opponent_agent = opponent_agent
        self.state_encoder = state_encoder
        self.action_encoder = action_encoder
        self.reward_policy = reward_policy
        self.exploration_policy = exploration_policy
        self.self_play = self_play
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def to_data(self):
        return {
            "environment": self.environment,
            "opponent_agent": self.opponent_agent,
            "state_encoder": self.state_encoder,
            "action_encoder": self.action_encoder,
            "reward_policy": self.reward_policy,
            "exploration_policy": self.exploration_policy,
            "self_play": self.self_play,
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
        }

    @staticmethod
    def from_data(data):
        return TabQLConfig(
            environment=data["environment"],
            opponent_agent=data["opponent_agent"],
            state_encoder=data["state_encoder"],
            action_encoder=data["action_encoder"],
            reward_policy=data["reward_policy"],
            exploration_policy=data["exploration_policy"],
            self_play=data["self_play"],
            learning_rate=data["learning_rate"],
            discount_factor=data["discount_factor"],
        )
