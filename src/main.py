from random import Random

from runner import Runner

from environments.azul.game import Game as AzulGame
from environments.tic_tac_toe.game import Game as TicTacToeGame

from interfaces.azul_console import AzulInputHandler
from interfaces.tic_tac_toe_console import TicTacToeInputHandler

from heuristics.azul_net_expected import AzulNetExpectedHeuristic

from agents.human import HumanAgent
from agents.random import RandomAgent

from agents.minimax.minimax import MinimaxAgent
from agents.minimax.minimax_alpha_beta import MinimaxAlphaBetaAgent
from agents.minimax.minimax_fixed_depth import MinimaxFixedDepthAgent
from agents.minimax.minimax_alpha_beta_ordering import MinimaxAlphaBetaOrderingAgent
from agents.minimax.minimax_iterative_deepening import MinimaxIterativeDeepeningAgent
from agents.minimax.policies.chance.sample_refills import SampleRefillsPolicy
from agents.minimax.policies.chance.round_termination import RoundTerminationPolicy
from agents.minimax.policies.ordering.point_based import PointBasedPolicy
from agents.minimax.policies.ordering.net_score_gain import NetScoreGainPolicy

from agents.mcts.mcts import MonteCarloTreeSearchAgent
from agents.mcts.mcts_reuse import MonteCarloTreeSearchReuseAgent
from agents.mcts.mcts_chance import MonteCarloTreeSearchChanceAgent
from agents.mcts.mcts_rollout import MonteCarloTreeSearchRolloutAgent
from agents.mcts.mcts_progressive_bias import MonteCarloTreeSearchProgressiveBiasAgent
from agents.mcts.mcts_heuristic_expansion import MonteCarloTreeSearchHeuristicExpansionAgent
from agents.mcts.mcts_progressive_widening import MonteCarloTreeSearchProgressiveWideningAgent
from agents.mcts.policies.chance.single_sample import SingleSamplePolicy
from agents.mcts.policies.rollout.point_epsilon import PointEpsilonPolicy
from agents.mcts.policies.rollout.score_estimate_epsilon import ScoreEstimateEpsilonPolicy
from agents.mcts.policies.expansion.point_based_random import PointBasedRandomExpansionPolicy
from agents.mcts.policies.expansion.score_estimate_random import ScoreEstimateRandomExpansionPolicy

from agents.rl.tabql.agent import TabqlAgent
from agents.rl.tabql.state_encoders.tic_tac_toe import TicTacToeStateEncoder

if __name__ == '__main__':
    game_seed = 42
    player_one_seed = 123
    player_two_seed = 456

    game = TicTacToeGame()
    # game = AzulGame(rng=Random(game_seed))
    player_one_agent = TabqlAgent(
        game,
        filename="q_table",
        state_encoder=TicTacToeStateEncoder(),
        # rng=Random(player_one_seed),
    )
    player_two_agent = MinimaxAgent(
        game,
    )
    runner = Runner(game, player_one_agent, player_two_agent)
    runner.run_game()
