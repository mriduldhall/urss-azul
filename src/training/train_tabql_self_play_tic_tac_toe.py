from environments.tic_tac_toe.game import Game as TicTacToeGame

from agents.rl.tabql.trainer import TabQLTrainer
from agents.rl.tabql.q_table import QTable
from agents.rl.tabql.state_encoders.tic_tac_toe import TicTacToeStateEncoder
from agents.rl.tabql.action_mapping.tic_tac_toe import TicTacToeActionMapping
from agents.rl.tabql.policies.action_selection.epsilon_greedy import EpsilonGreedyActionSelection
from agents.rl.tabql.policies.action_selection.softmax import SoftmaxActionSelection
from agents.rl.tabql.policies.rewards.outcome import OutcomeReward
from agents.rl.tabql.config import TabQLConfig

class Trainer:
    @staticmethod
    def create():
        game_constructor = TicTacToeGame
        opponent_constructor = None
        state_encoder = TicTacToeStateEncoder()
        action_encoder = None
        action_mapping = TicTacToeActionMapping()
        reward_policy = OutcomeReward()
        exploration_policy = EpsilonGreedyActionSelection(epsilon=0.1)
        self_play = True
        learning_rate = 0.1
        discount_factor = 0.9

        config = TabQLConfig(
            environment=game_constructor().get_config(),
            opponent_agent=opponent_constructor(game_constructor()).get_config() if not self_play else None,
            state_encoder=state_encoder.get_config(),
            action_encoder=action_encoder.get_config() if action_encoder else None,
            action_mapping=action_mapping.get_config(),
            reward_policy=reward_policy.get_config(),
            exploration_policy=exploration_policy.get_config(),
            self_play=self_play,
            learning_rate=learning_rate,
            discount_factor=discount_factor,
        )

        return TabQLTrainer(
            config,
            game_constructor,
            opponent_constructor,
            QTable(action_count=9, action_mapping=action_mapping),
            state_encoder,
            SoftmaxActionSelection(5, 0.9999),
            OutcomeReward(),
        )
