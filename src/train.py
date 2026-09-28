from training.train_tabql_tic_tac_toe import Trainer as TicTacToeTabqlTrainer
from agents.random import RandomAgent
from agents.rl.tabql.checkpoint_store import TabQLCheckpointStore

if __name__ == '__main__':
    checkpoint_path = "checkpoint.json"
    q_table_path = "q_table.json"

    opponent_constructor = lambda game: RandomAgent(game)

    trainer = TicTacToeTabqlTrainer.create(opponent_constructor)
    trainer.run_training(100000)
    checkpoint = trainer.create_checkpoint()
    TabQLCheckpointStore.save(checkpoint_path, checkpoint)

    q_table = trainer.q_table
    q_table.save(q_table_path)
