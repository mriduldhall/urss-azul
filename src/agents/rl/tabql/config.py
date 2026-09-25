class TabQLConfig:
    def __init__(self, environment, state_encoder, action_encoder, reward_policy, exploration_policy, self_play, learning_rate, discount_factor):
        self.environment = environment
        self.state_encoder = state_encoder
        self.action_encoder = action_encoder
        self.reward_policy = reward_policy
        self.exploration_policy = exploration_policy
        self.self_play = self_play
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
