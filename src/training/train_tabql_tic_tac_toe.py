from environments.tic_tac_toe.game import Game as TicTacToeGame

from agents.rl.tabql.trainer import TabQLTrainer
from agents.rl.tabql.q_table import QTable
from agents.rl.tabql.state_encoders.tic_tac_toe import TicTacToeStateEncoder
from agents.rl.tabql.policies.action_selection.epsilon_greedy import EpsilonGreedyActionSelection
from agents.rl.tabql.policies.action_selection.softmax import SoftmaxActionSelection
from agents.rl.tabql.policies.rewards.outcome import OutcomeReward

class Trainer:
    @staticmethod
    def train(opponent_constructor):
        game_constructor = TicTacToeGame

        trainer = TabQLTrainer(
            game_constructor,
            False,
            opponent_constructor,
            QTable(action_count=9),
            TicTacToeStateEncoder(),
            SoftmaxActionSelection(5, 0.9999),
            OutcomeReward(),
            learning_rate=0.1,
            discount_factor=0.9,
        )
        q_table = trainer.run_training(100000)
        return q_table
