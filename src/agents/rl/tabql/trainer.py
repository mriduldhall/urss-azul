from random import Random

class TabQLTrainer:
    def __init__(
            self,
            game_constructor,
            opponent_agent_constructor,
            q_table,
            state_encoder,
            action_selection_policy,
            reward_policy,
            episodes,
            learning_rate=0.1,
            discount_factor=0.9,
            rng=None
    ):
        self.game_constructor = game_constructor
        self.opponent_agent_constructor = opponent_agent_constructor
        self.q_table = q_table
        self.state_encoder = state_encoder
        self.action_selection_policy = action_selection_policy
        self.reward_policy = reward_policy
        self.episodes = episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.rng = rng if rng is not None else Random()

    def run_episode(self, episode_number, learner_starts=True):
        game = self.game_constructor()
        opponent_agent = self.opponent_agent_constructor(game)
        is_learner_turn = learner_starts

        while not game.check_end():
            if is_learner_turn:
                state = self.state_encoder.encode(game)
                move = self.action_selection_policy.choose_action(state, self.q_table, game.get_legal_actions(), self.rng, episode_number)

                acting_player = game.current_player
                game.make_move(move)
                reward = self.reward_policy.get_reward(game, acting_player)

                if game.check_end():
                    target = reward
                else:
                    next_state = self.state_encoder.encode(game)
                    next_best_q_value = max(self.q_table.get_value(next_state, action) for action in game.get_legal_actions())
                    target = reward - (self.discount_factor * next_best_q_value)

                self.q_table.update(state, move, target, self.learning_rate)
            else:
                move = opponent_agent.make_move()
                game.make_move(move)

            is_learner_turn = not is_learner_turn

    def run_training(self):
        is_learner_starts = True
        for episode in range(self.episodes):
            self.run_episode(episode, learner_starts=is_learner_starts)
            is_learner_starts = not is_learner_starts

        return self.q_table
