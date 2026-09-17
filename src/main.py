from random import Random
from agents.human import HumanAgent
from agents.random import RandomAgent
from agents.minimax.minimax import MinimaxAgent
from agents.mcts.mcts import MonteCarloTreeSearchAgent
from agents.mcts.mcts_chance import MonteCarloTreeSearchChanceAgent
from agents.mcts.mcts_rollout import MonteCarloTreeSearchRolloutAgent
from agents.minimax.minimax_alpha_beta import MinimaxAlphaBetaAgent
from agents.minimax.minimax_fixed_depth import MinimaxFixedDepthAgent
from agents.minimax.minimax_alpha_beta_ordering import MinimaxAlphaBetaOrderingAgent
from agents.minimax.minimax_iterative_deepening import MinimaxIterativeDeepeningAgent
from environments.azul.game import Game as AzulGame
from environments.tic_tac_toe.game import Game as TicTacToeGame
from interfaces.azul_console import AzulInputHandler
from interfaces.tic_tac_toe_console import TicTacToeInputHandler
from heuristics.azul_net_expected import AzulNetExpectedHeuristic
from chance_policies.azul.round_termination import RoundTerminationPolicy
from chance_policies.azul.sample_refills import SampleRefillsPolicy
from chance_policies.azul.mcts_single_sample import SingleSamplePolicy
from order_policies.azul.net_score_gain import NetScoreGainPolicy
from order_policies.azul.point_based import PointBasedPolicy
from rollout_policies.azul.point_epsilon import PointEpsilonPolicy
from runner import Runner

if __name__ == '__main__':
    game_seed = 42
    player_one_seed = 123
    player_two_seed = 456

    # game = AzulGame()
    game = AzulGame(rng=Random(game_seed))
    player_one_agent = MonteCarloTreeSearchRolloutAgent(
        game,
        simulations=1000,
        rng=Random(player_one_seed),
        chance_policy=SingleSamplePolicy(rng=Random(player_one_seed)),
        rollout_policy=PointEpsilonPolicy(epsilon=0.1)
    )
    player_two_agent = MinimaxIterativeDeepeningAgent(
        game,
        heuristic=AzulNetExpectedHeuristic(),
        time_limit=5,
        max_depth=10,
        chance_policy=SampleRefillsPolicy(samples=5, rng=Random(player_two_seed)),
        ordering_policy=PointBasedPolicy(),
    )
    runner = Runner(game, player_one_agent, player_two_agent)
    runner.run_game()
