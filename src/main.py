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
from chance_policies.azul.round_termination import RoundTerminationPolicy
from runner import Runner

if __name__ == '__main__':
    game_seed = 42
    player_one_seed = 123
    player_two_seed = 456

    # game = AzulGame()
    game = AzulGame(rng=Random(game_seed))
    player_one_agent = MinimaxFixedDepthAgent(game, heuristic=AzulNetExpectedHeuristic(), max_depth=2, chance_policy=RoundTerminationPolicy())
    player_two_agent = RandomAgent(game, rng=Random(player_two_seed))
    runner = Runner(game, player_one_agent, player_two_agent)
    runner.run_game()
