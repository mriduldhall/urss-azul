from random import Random
from agents.human import HumanAgent
from agents.random import RandomAgent
from agents.minimax import MinimaxAgent
from agents.mcts import MonteCarloTreeSearchAgent
from agents.minimax_fixed_depth import MinimaxFixedDepthAgent
from environments.azul.game import Game as AzulGame
from environments.tic_tac_toe.game import Game as TicTacToeGame
from interfaces.azul_console import AzulInputHandler
from interfaces.tic_tac_toe_console import TicTacToeInputHandler
from heuristics.azul_net_expected import AzulNetExpectedHeuristic
from runner import Runner


if __name__ == '__main__':
    game_seed = 42

    # game = AzulGame()
    game = AzulGame(rng=Random(game_seed))
    player_one_agent = MinimaxFixedDepthAgent(game, AzulNetExpectedHeuristic(), max_depth=3)
    player_two_agent = RandomAgent(game)
    runner = Runner(game, player_one_agent, player_two_agent)
    runner.run_game()
