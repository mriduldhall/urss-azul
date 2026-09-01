from agents.human import HumanAgent
from agents.random import RandomAgent
from agents.minimax import MinimaxAgent
from agents.mcts import MonteCarloTreeSearchAgent
from environments.tic_tac_toe.game import Game
from interfaces.tic_tac_toe_console import TicTacToeInputHandler
from runner import Runner


if __name__ == '__main__':
    game = Game()
    player_one_agent = MonteCarloTreeSearchAgent(game)
    player_two_agent = HumanAgent(TicTacToeInputHandler(game))
    runner = Runner(game, player_one_agent, player_two_agent)
    runner.run_game()
