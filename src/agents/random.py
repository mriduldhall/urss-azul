from random import Random

class RandomAgent:
    def __init__(self, game, rng=None):
        self.game = game
        self.rng = rng if rng is not None else Random()

    def make_move(self):
        return self.rng.choice(self.game.get_legal_actions())
