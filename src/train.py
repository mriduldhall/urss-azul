from pathlib import Path
from agents.random import RandomAgent
from training.train_tabql_tic_tac_toe import Trainer as TicTacToeTabqlTrainer
from agents.rl.tabql.checkpoint_store import TabQLCheckpointStore

if __name__ == '__main__':
    checkpoint_path = Path("checkpoint.json")
    q_table_path = Path("q_table.json")

    opponent_constructor = lambda game: RandomAgent(game)

    trainer = TicTacToeTabqlTrainer.create(opponent_constructor)

    if checkpoint_path.exists():
        checkpoint = TabQLCheckpointStore().load(checkpoint_path)
        trainer.restore(checkpoint)

    trainer.run_training(100000)
    checkpoint = trainer.create_checkpoint()
    TabQLCheckpointStore.save(checkpoint_path, checkpoint)

    q_table = trainer.q_table
    q_table.save(q_table_path)
