from random import Random

#noinspection DuplicatedCode
class TabQLTrainer:
    def __init__(
            self,
            game_constructor,
            self_play,
            opponent_agent_constructor,
            q_table,
            state_encoder,
            action_selection_policy,
            reward_policy,
            learning_rate=0.1,
            discount_factor=0.9,
            rng=None
    ):
        self.game_constructor = game_constructor
        self.self_play = self_play
        self.opponent_agent_constructor = opponent_agent_constructor
        self.q_table = q_table
        self.state_encoder = state_encoder
        self.action_selection_policy = action_selection_policy
        self.reward_policy = reward_policy
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.rng = rng if rng is not None else Random()
        self.completed_episodes = 0
        self.next_learner_starts = True
        if self_play and opponent_agent_constructor is not None:
            raise ValueError("If self_play is True, opponent_agent_constructor must be None.")
        if not self_play and opponent_agent_constructor is None:
            raise ValueError("If self_play is False, opponent_agent_constructor must be provided.")

    def find_target(self, game, reward):
        if game.check_end():
            return reward

        next_state = self.state_encoder.encode(game)
        next_best_q_value = max(
            self.q_table.get_value(next_state, action) for action in game.get_legal_actions())
        return reward - (self.discount_factor * next_best_q_value)

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

                target = self.find_target(game, reward)

                self.q_table.update(state, move, target, self.learning_rate)
            else:
                move = opponent_agent.make_move()
                game.make_move(move)

            is_learner_turn = not is_learner_turn

    def run_self_play_episode(self, episode_number):
        game = self.game_constructor()

        while not game.check_end():
            state = self.state_encoder.encode(game)
            move = self.action_selection_policy.choose_action(state, self.q_table, game.get_legal_actions(), self.rng, episode_number)

            acting_player = game.current_player
            game.make_move(move)
            reward = self.reward_policy.get_reward(game, acting_player)

            target = self.find_target(game, reward)

            self.q_table.update(state, move, target, self.learning_rate)

    def run_training(self, episodes):
        for episode in range(episodes):
            current_episode = self.completed_episodes

            if self.self_play:
                self.run_self_play_episode(current_episode)
            else:
                self.run_episode(current_episode, learner_starts=self.next_learner_starts)

            self.next_learner_starts = not self.next_learner_starts
            self.completed_episodes += 1

        return self.q_table
