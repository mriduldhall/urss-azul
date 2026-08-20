from agents.human import HumanAgent
from agents.random import RandomAgent
from environments.tic_tac_toe.game import Game
from runner import Runner


if __name__ == '__main__':
    game = Game()
    player_one_agent = HumanAgent(game)
    player_two_agent = RandomAgent(game)
    runner = Runner(game, player_one_agent, player_two_agent)
    runner.run_game()
