from environments.azul.game import Game as AzulGame

from agents.rl.tabql.trainer import TabQLTrainer
from agents.rl.tabql.q_table import QTable
from agents.rl.tabql.state_encoders.azul import AzulStateEncoder
from agents.rl.tabql.policies.action_selection.epsilon_greedy import EpsilonGreedyActionSelection
from agents.rl.tabql.action_mapping.azul import AzulActionMapping
from agents.rl.tabql.policies.rewards.outcome import OutcomeReward
from agents.rl.tabql.config import TabQLConfig

class Trainer:
    @staticmethod
    def create(opponent_constructor):
        game_constructor = AzulGame
        state_encoder = AzulStateEncoder()
        action_mapping = AzulActionMapping()
        reward_policy = OutcomeReward()
        exploration_policy = EpsilonGreedyActionSelection(0.1)
        self_play = False
        learning_rate = 0.1
        discount_factor = 0.9

        config = TabQLConfig(
            environment=game_constructor().get_config(),
            opponent_agent=opponent_constructor(game_constructor()).get_config() if not self_play else None,
            state_encoder=state_encoder.get_config(),
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
            QTable(action_count=180, action_mapping=action_mapping),
            state_encoder,
            action_mapping,
            exploration_policy,
            OutcomeReward(),
        )
