from training.train_tabql_self_play_tic_tac_toe import Trainer as TicTacToeTabqlSelfPlayTrainer

if __name__ == '__main__':
    q_table = TicTacToeTabqlSelfPlayTrainer.train()
    q_table.save("q_table")
    print("Training completed.")
