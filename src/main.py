from agents.human import HumanAgent
from agents.random import RandomAgent
from agents.minimax import MinimaxAgent
from agents.mcts import MonteCarloTreeSearchAgent
from environments.azul.game import Game as AzulGame
from environments.tic_tac_toe.game import Game as TicTacToeGame
from interfaces.azul_console import AzulInputHandler
from interfaces.tic_tac_toe_console import TicTacToeInputHandler
from runner import Runner


if __name__ == '__main__':
    game = AzulGame()
    player_one_agent = HumanAgent(AzulInputHandler(game))
    player_two_agent = HumanAgent(AzulInputHandler(game))
    runner = Runner(game, player_one_agent, player_two_agent)
    runner.run_game()
