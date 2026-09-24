from environments.tic_tac_toe.game import Game as TicTacToeGame

from agents.rl.tabql.trainer import TabQLTrainer
from agents.rl.tabql.q_table import QTable
from agents.rl.tabql.state_encoders.tic_tac_toe import TicTacToeStateEncoder
from agents.rl.tabql.policies.action_selection.epsilon_greedy import EpsilonGreedyActionSelection
from agents.rl.tabql.policies.action_selection.softmax import SoftmaxActionSelection
from agents.rl.tabql.policies.rewards.outcome import OutcomeReward

class Trainer:
    @staticmethod
    def train():
        game_constructor = TicTacToeGame

        trainer = TabQLTrainer(
            game_constructor,
            True,
            None,
            QTable(action_count=9),
            TicTacToeStateEncoder(),
            EpsilonGreedyActionSelection(epsilon=0.1),
            OutcomeReward(),
            episodes=100000,
            learning_rate=0.1,
            discount_factor=0.9,
        )
        q_table = trainer.run_training()
        return q_table
