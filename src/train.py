from training.train_tabql_tic_tac_toe import Trainer as TicTacToeTabqlTrainer
from agents.random import RandomAgent

if __name__ == '__main__':
    opponent_constructor = lambda game: RandomAgent(game)
    q_table = TicTacToeTabqlTrainer.train(opponent_constructor)
    print("Training completed.")
