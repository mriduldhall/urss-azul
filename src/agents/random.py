from random import choice


class RandomAgent:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        return choice(self.game.get_legal_actions())